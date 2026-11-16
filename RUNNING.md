# Running Provenance Guard

Provenance Guard is a web service that guesses whether a piece of writing was
written by a person or by an AI. **It is not hosted anywhere. There is no public
URL.** You run it on your own machine, and it answers at:

```
http://127.0.0.1:5000
```

That address means "this computer only." The URL exists because you start the
service yourself with the command below, and it stops existing when you stop it.
It uses no API key, account or internet connection once set up: the model that
reads your text runs on your own laptop.

---

## What your machine needs

| Need | Detail |
|---|---|
| Python | **3.11, 3.12 or 3.13.** Not 3.14 (the pinned packages break) and not 3.10 or older |
| Disk | About 9 GB free (`torch` is most of it; the model adds about 550 MB) |
| RAM | 4 GB or more |
| Internet | Only for the one-time install and model download |
| A terminal | macOS/Linux: Terminal. Windows: PowerShell or Git Bash |

---

## Setup (once)

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python detector.py                 # downloads the model (~550 MB) and scores a sample
python test.py                     # checks your setup
```

**Setup worked when `python test.py` passes.**

- `python detector.py` is slow the first time because it downloads the model.
  You'll see `[WARN] Detector model — not downloaded yet` in `test.py` until you
  have run it.
- Every new terminal needs `source .venv/bin/activate` again before the
  commands below (your prompt shows `(.venv)` when it is active).

---

## Start the service

```bash
python app.py
```

You should see:

```
Provenance Guard on http://127.0.0.1:5000
  detector model:  gpt2
  rate limiting:   ON
  audit log:       .../logs/audit.jsonl
```

**Leave this terminal open.** It is the server. Press `Ctrl+C` to stop it. Use
a **second terminal** (activate `.venv` there too if you will run Python
scripts) for everything below.

The first submission takes 10 to 20 seconds while the model loads into memory.
After that, each takes a second or two.

To use a different port or address:

```bash
PORT=8000 python app.py            # then use http://127.0.0.1:8000
```

Windows PowerShell: `$env:PORT=8000; python app.py`.

---

## Use it

### 1. Check it's alive

```bash
curl -X POST http://127.0.0.1:5000/ping \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

Expected: `{"ok": true, "service": "provenance-guard", "you_sent": "hello"}`.

`curl http://127.0.0.1:5000/health` shows whether the model is loaded and
whether rate limiting is on.

> **Windows PowerShell:** `curl` is a different tool there. Use `curl.exe`, put
> the whole command on one line, and escape the inner quotes:
> `curl.exe -X POST http://127.0.0.1:5000/ping -H "Content-Type: application/json" -d '{\"message\": \"hello\"}'`.
> Git Bash needs no change.

### 2. Submit some writing

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The committee reviewed the proposal and decided to postpone the vote until spring, citing concerns about the budget.", "creator_id": "me"}'
```

You get back:

```json
{
  "content_id": "b474cde8-653b-443c-abcb-183584b07e3a",
  "guess": "unsure",
  "confidence": 0.5972,
  "label": "We can't tell whether this was written by a person or by AI. ...",
  "model_score": 0.7222,
  "style_score": 0.4722
}
```

| Field | Meaning |
|---|---|
| `guess` | `ai`, `human` or `unsure`. The system prefers `unsure` to a wrong `ai`, because wrongly accusing a real writer costs more than missing an AI text |
| `confidence` | The combined score from 0 to 1. Above 0.65 leans AI, below 0.35 leans human |
| `label` | The plain-language message a reader would see |
| `model_score`, `style_score` | The two signals behind the guess (predictability to a language model, and the shape of the writing) |
| `content_id` | Keep this. You need it to appeal |

`creator_id` is any string that names who is writing. Texts need to be real
English prose, at most 5000 characters.

### 3. Appeal a decision

If a result is wrong, send the `content_id` from the submission and a reason:

```bash
curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "PASTE-THE-ID-HERE", "reasoning": "I wrote this myself for class."}'
```

The decision is marked `under_review`. The original decision is kept and the
appeal is recorded beside it.

### 4. Read the audit log

```bash
curl "http://127.0.0.1:5000/log?limit=10"
```

Every decision, rejection and appeal is recorded (in `logs/audit.jsonl`).

---

## The routes

| Route | What it does |
|---|---|
| `POST /ping` | Is the service answering |
| `GET /health` | Is the service up, which model, is it loaded, is rate limiting on |
| `POST /submit` | Score a text. Body `{"text", "creator_id"}` |
| `POST /appeal` | Appeal a decision. Body `{"content_id", "reasoning"}` |
| `GET /log` | The audit log as JSON. Optional `?limit=N` |

---

## When you're sent away: errors and rate limits

A bad request gets a `4xx` with `{"error": ..., "message": ...}` and is never
scored. It is still written to the audit log.

| Status | `error` | Cause |
|---|---|---|
| 400 | `invalid_body` / `missing_text` / `text_not_a_string` / `empty_text` | Body is not a JSON object, or `text` is missing, not a string, or blank |
| 413 | `text_too_long` | Over 5000 characters |
| 422 | `no_readable_text` / `text_too_short` | No English words, or too short for the model to score |
| 429 | `rate_limited` | Too many requests (see below) |

**Rate limits on `/submit`:**

- **5 per minute and 50 per day for each `creator_id`.**
- **20 per minute and 200 per day for each address**, no matter how many
  `creator_id`s are used.

A `429` tells you how to recover:

- The `Retry-After` header holds the seconds to wait.
- The body has `retry_after` (same number), `scope` (`creator` or `address`, so
  you know which limit you hit) and `"evaluated": false`. That last field means
  **the text was not checked.** A `429` is never a "human" verdict.

Wait that many seconds, then send again. Counts are kept in memory, so
restarting the service clears them.

---

## Scripts

Run with the service already started in another terminal.

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment |
| `python detector.py "some text"` | Score one text with signal one, no server needed |
| `python stylometry.py "some text"` | Score one text with signal two, no server needed |
| `python run_attacks.py --flood 15` | Send 15 submissions from one `creator_id` and print the status codes (`200`s then `429`s). Writes `results/flood_<date>.md` |
| `python run_attacks.py --set attack_set` | Run the attack set. **Most rows will return `429` from one address**, because of the address limit |
| `python run_eval.py --label before` | Run the five criteria, three trials |
| `python -m unittest test_rate_limit -v` | The rate-limit tests. They stub the model and use a temporary log, so they need no server and don't touch `logs/audit.jsonl` |

> The scripts and the service both write to `logs/` and `results/`. Those
> folders are evidence, so they are committed on purpose.

---

## Running it for real (optional)

Flask's built-in server is for development. A production-style server:

```bash
HOST=0.0.0.0 gunicorn app:app --bind 0.0.0.0:${PORT:-5000}
```

| Variable | Default | What it does |
|---|---|---|
| `HOST` | `127.0.0.1` | `127.0.0.1` is your machine only. Use `0.0.0.0` so other machines can reach it |
| `PORT` | `5000` | The port to listen on |
| `AI201_DEBUG` | `1` | Debug mode. It turns itself off whenever `HOST` isn't `127.0.0.1` or `localhost` |

**This will not fit a free hosting tier.** `torch` plus the `gpt2` weights need
well over the 512 MB a free tier gives, and a free host has no persistent disk,
so the 550 MB download repeats after every spin-down. Run it locally.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `python: command not found` / wrong version | Use `python3`, and check `python3 --version` is 3.11 to 3.13 |
| `ModuleNotFoundError: flask` (or `flask_limiter`, `torch`) | The virtual environment isn't active, or `pip install -r requirements.txt` didn't finish. Run `source .venv/bin/activate`, then the install again |
| `curl: (7) Failed to connect` | The server isn't running, or it's on another port. Check the first terminal |
| `Address already in use` | An earlier server is still running. Stop it (`Ctrl+C` in its terminal) or start on another port with `PORT=8000` |
| `DetectorUnavailable` | The model isn't downloaded. Run `python detector.py` once |
| The first submission takes 10+ seconds | The model is loading into memory. Later ones are faster |
| *Every* submission is slow | `GET /health` shows `detector_loaded`. If it keeps going back to `false`, the model is reloading each call |
| `404` from curl | Check the path is exactly `/submit`, `/appeal`, `/log`, `/health` or `/ping` |
| Request body arrives empty / `invalid_body` | curl needs `-H "Content-Type: application/json"` and a JSON object body |
| `Cannot bind parameter 'Headers'` | You're in PowerShell. Use `curl.exe` on one line |
| `429` on a run script | You hit the rate limit. Wait `Retry-After` seconds, or restart the service to clear the counts |
| `/appeal` returns `404 unknown_content_id` | The `content_id` isn't in the log. Copy it exactly from the `/submit` response |

If `/submit` fails, check `/ping` still answers. If it does, the service is up
and the problem is in the request. If it doesn't, the service itself isn't
running.

---

## Where things live

| File | What it does |
|---|---|
| `app.py` | The service and its routes |
| `config.py` | Every setting: host, port, thresholds, weights, rate limits, the model |
| `detector.py` | Signal one, the local language model |
| `stylometry.py` | Signal two, the shape of the writing |
| `scoring.py` | Combines the signals and picks the label |
| `audit.py` | The append-only audit log writer |
| `run_attacks.py`, `run_eval.py`, `scenarios.py` | The test scripts |
| `criteria.md` | The five criteria the system is judged on |
| `logs/audit.jsonl` | The audit log |
| `results/` | Attack and eval run output |
| `README.md` | The design, the evidence and what's still broken |
