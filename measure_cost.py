#!/usr/bin/env python3
"""
Measure what one /submit run costs, and exercise the failure paths.

    python measure_cost.py

The real cost of this system is compute on your own machine: there is no API
spend and no tokens billed. So it measures seconds, two ways, per run:

  wall  seconds on a clock (time.perf_counter) around the whole request
  cpu   CPU seconds the process burned (time.process_time), all threads

It runs the real gpt2 model in-process through Flask's test client (no network),
sends 10 different texts, and averages. The first call loads the model, so it is
timed on its own and NOT in the average (a running service pays it once).

Records go to logs/instrumentation_run.jsonl, not the real audit log, so this
never adds to logs/audit.jsonl. The summary goes to results/cost_run.md.
"""

import json
import platform
import statistics
import time
from datetime import date
from pathlib import Path
from unittest import mock

import config

ROOT = Path(__file__).parent
RUN_LOG = ROOT / "logs" / "instrumentation_run.jsonl"
SUMMARY = ROOT / "results" / "cost_run.md"

# Redirect BEFORE importing app, so nothing leaks into the real audit log.
RUN_LOG.parent.mkdir(exist_ok=True)
RUN_LOG.write_text("", encoding="utf-8")
config.AUDIT_LOG = RUN_LOG

import app as app_module  # noqa: E402
import detector  # noqa: E402

TEXTS = [
    "Okay so — the dog ate my sandwich. Not a metaphor. Actual sandwich, actual dog (Biscuit, a menace). I turned around for ten seconds to answer the door and when I came back there was just a crust and a very guilty face. Dinner was cereal. Again.",
    "Technology plays an important role in modern education. It helps students learn new skills and access useful information. It also helps teachers share lessons and track student progress. Technology makes learning more engaging and more accessible for everyone. It is important for schools to use technology in a thoughtful way. This helps students prepare for the future and succeed in their careers.",
    "The committee convened on Tuesday to consider the proposed amendments to the municipal zoning ordinance. After extended deliberation, it was resolved that the residential density limits would remain unchanged, pending a further review of infrastructure capacity. Several members expressed reservations regarding the projected burden on existing water and sewage services; these concerns will be addressed in the subsequent report, which is expected before the close of the fiscal year.",
    "Remote work has changed how many people think about their jobs. It offers flexibility and saves commuting time, but it can also blur the line between work and home. Some people love it. Others miss the office more than they expected, honestly. Companies are still working out what a good balance looks like, and I suspect they will be for a while yet.",
    "I like my dog. He is brown and he is big. He likes to run in the park. We play with a ball every day. He is a good dog and I love him very much.",
    "Effective communication is a cornerstone of successful teamwork. When team members share information openly, they build trust and avoid misunderstandings. Clear communication also helps teams solve problems faster and adapt to change.",
    "My grandmother kept a tin of buttons she never used, and when she died we found out why: every button was from a coat somebody had worn out of her life. She could tell you whose. I took the tin. I still can't sew.",
    "The results indicate a statistically significant improvement in retention among participants who received the intervention, although the effect size was modest and the follow-up period was short. Further research with larger and more diverse samples is warranted before drawing firm conclusions.",
    "Went to the market early, before the heat. Bought peaches, too many, and a loaf that was still warm. The woman at the stall called me honey and gave me a plum for free. Small things. They add up to a decent Saturday.",
    "Climate change is one of the most pressing challenges of our time. It affects ecosystems, economies, and communities around the world. Addressing it requires cooperation between governments, businesses, and individuals. By taking action now, we can create a more sustainable future for generations to come.",
]


def main():
    client = app_module.app.test_client()
    print("Cold start (model load + first run), not in the average:")
    t0 = time.perf_counter()
    c0 = time.process_time()
    r = client.post("/submit", json={"text": TEXTS[0], "creator_id": "cold_start"})
    cold_wall = time.perf_counter() - t0
    cold_cpu = time.process_time() - c0
    print(f"  status {r.status_code}  wall {cold_wall:.2f}s  cpu {cold_cpu:.2f}s")

    print("\n10 warm runs:")
    walls, cpus, chars = [], [], []
    for i, text in enumerate(TEXTS, 1):
        t0 = time.perf_counter()
        c0 = time.process_time()
        r = client.post("/submit", json={"text": text, "creator_id": f"cost_probe_{i}"})
        wall = time.perf_counter() - t0
        cpu = time.process_time() - c0
        assert r.status_code == 200, r.get_json()
        walls.append(wall)
        cpus.append(cpu)
        chars.append(len(text))
        print(f"  run {i:2d}: {len(text):4d} chars  wall {wall:.3f}s  cpu {cpu:.3f}s")

    print("\nFailure paths (each should leave a record):")
    app_module.limiter.reset()
    failures = []

    def fail(name, resp):
        failures.append((name, resp.status_code))
        print(f"  {name}: {resp.status_code}")

    fail("empty text", client.post("/submit", json={"text": "  ", "creator_id": "fail_empty"}))
    fail("missing text", client.post("/submit", json={"creator_id": "fail_missing"}))
    fail("text too long", client.post("/submit", json={"text": "word " * 2000, "creator_id": "fail_long"}))
    fail("body is not a JSON object", client.post("/submit", json=["not", "an", "object"]))
    fail("no readable words", client.post("/submit", json={"text": "🙂🙂🙂 ???", "creator_id": "fail_emoji"}))
    with mock.patch.object(detector, "model_signal", side_effect=detector.DetectorUnavailable("model files missing")):
        fail("detector unavailable", client.post("/submit", json={"text": TEXTS[1], "creator_id": "fail_detector"}))
    with mock.patch.object(detector, "model_signal", side_effect=RuntimeError("simulated crash in signal one")):
        fail("unexpected exception", client.post("/submit", json={"text": TEXTS[1], "creator_id": "fail_crash"}))
    for _ in range(config.RATE_LIMIT_PER_MINUTE + 1):
        resp = client.post("/submit", json={"text": TEXTS[4], "creator_id": "fail_flood"})
    fail("rate limit", resp)

    mean_wall = statistics.mean(walls)
    mean_cpu = statistics.mean(cpus)
    lines = [
        f"# Cost of one /submit run — measured {date.today().isoformat()}",
        "",
        f"- Machine: {platform.platform()}, Python {platform.python_version()}, model `{config.DETECTOR_MODEL}` on CPU",
        f"- Method: `python measure_cost.py`. Real model, Flask test client in-process, 10 different texts "
        f"({min(chars)}–{max(chars)} characters, mean {statistics.mean(chars):.0f}), model already loaded.",
        "- Wall time is `time.perf_counter()` around the request. CPU time is `time.process_time()` "
        "(all threads) over the same span.",
        f"- **Mean wall per run: {mean_wall:.3f} s** (min {min(walls):.3f}, max {max(walls):.3f}, "
        f"stdev {statistics.stdev(walls):.3f})",
        f"- **Mean CPU per run: {mean_cpu:.3f} s** (min {min(cpus):.3f}, max {max(cpus):.3f})",
        f"- Cold start (first request, loads the model), not averaged: wall {cold_wall:.2f} s, cpu {cold_cpu:.2f} s",
        "- API spend: $0 (nothing is called over the network).",
        "",
        "| run | chars | wall s | cpu s |",
        "|---|---|---|---|",
    ]
    lines += [f"| {i} | {c} | {w:.3f} | {p:.3f} |" for i, (c, w, p) in enumerate(zip(chars, walls, cpus), 1)]
    lines += ["", "Failure paths exercised: " + ", ".join(f"{n} → {s}" for n, s in failures)]
    SUMMARY.parent.mkdir(exist_ok=True)
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\nMean wall {mean_wall:.3f}s, mean cpu {mean_cpu:.3f}s over 10 runs")
    print(f"Log:     {RUN_LOG}")
    print(f"Summary: {SUMMARY}")


if __name__ == "__main__":
    main()
