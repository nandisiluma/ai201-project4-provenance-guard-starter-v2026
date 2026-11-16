# Cost of one /submit run — measured 2026-11-16

- Machine: macOS-26.6.2-x86_64-i386-64bit, Python 3.12.14, model `gpt2` on CPU
- Method: `python measure_cost.py`. Real model, Flask test client in-process, 10 different texts (144–485 characters, mean 289), model already loaded.
- Wall time is `time.perf_counter()` around the request. CPU time is `time.process_time()` (all threads) over the same span.
- **Mean wall per run: 0.123 s** (min 0.093, max 0.168, stdev 0.027)
- **Mean CPU per run: 0.455 s** (min 0.365, max 0.616)
- Cold start (first request, loads the model), not averaged: wall 8.13 s, cpu 6.72 s
- API spend: $0 (nothing is called over the network).

| run | chars | wall s | cpu s |
|---|---|---|---|
| 1 | 244 | 0.120 | 0.475 |
| 2 | 400 | 0.137 | 0.536 |
| 3 | 485 | 0.158 | 0.616 |
| 4 | 351 | 0.145 | 0.567 |
| 5 | 144 | 0.098 | 0.385 |
| 6 | 234 | 0.093 | 0.365 |
| 7 | 213 | 0.103 | 0.407 |
| 8 | 295 | 0.168 | 0.380 |
| 9 | 216 | 0.099 | 0.394 |
| 10 | 306 | 0.108 | 0.424 |

Failure paths exercised: empty text → 400, missing text → 400, text too long → 413, body is not a JSON object → 400, no readable words → 422, detector unavailable → 503, unexpected exception → 500, rate limit → 429
