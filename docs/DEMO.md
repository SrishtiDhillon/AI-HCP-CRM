# 90-second walkthrough

Use only the fictional seed record. This is a recording guide; it does not claim a video has been recorded.

1. **0–15 seconds:** Explain the two paths: deterministic form writes and optional conversational AI.
2. **15–35 seconds:** Start the backend, run `python scripts/seed_demo.py`, open the frontend, and enter the printed HCP ID, today's interaction date, and `Discussed an example product demo`. Leave follow-up blank. Submit and show the saved interaction ID.
3. **35–50 seconds:** Enter HCP ID `999999` with a new summary. Submit; show `HCP not found` and that your input remains available to correct.
4. **50–65 seconds:** With no Groq key configured, send a chat message and show the explicit unavailable-chat response. Explain that the form remains independent of AI.
5. **65–80 seconds:** Run `python -m pytest backend/tests -q` and `npm test` in the frontend directory. Explain one regression test rather than merely citing a count.
6. **80–90 seconds:** State limitations: local prototype, SQLite tests, optional live AI unverified, no authentication or exactly-once agent writes.

For the automated API-only walkthrough, run `python scripts/demo.py`. The checked-in GIF is generated from its captured responses and is labeled as an API demo.
