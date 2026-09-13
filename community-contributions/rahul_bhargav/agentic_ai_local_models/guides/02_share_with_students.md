# Share this course with students

Students need the **entire folder** (labs + `shared/` + `6_mcp/servers/`). A single notebook from Week 2 onward will fail to import.

## Option A — GitHub (best)

1. Create a repo (public or private with school GitHub).
2. Put **this inner course directory** at the repo root (`README.md`, `1_foundations/`, `shared/`, …).
3. Send the clone URL plus `START_HERE.md`.
4. Optional: GitHub Classroom assignment from the repo.

`.gitignore` already skips venvs and notebook checkpoints.

## Option B — Zip + Drive / LMS

1. Zip the course root (the folder that contains `START_HERE.md`).
2. Upload to Drive / Moodle / Teams.
3. Tell students: Colab → upload zip → unzip → `chdir` into the folder (commands are in `START_HERE.md`).

Do **not** zip only `1_foundations`.

## Option C — Colab copies

You can still **File → Save a copy in Drive** for Lab 1 (it is self-contained). For later weeks, prefer A or B so `shared/course_runtime.py` is on disk.

## What to say on day 0

- No paid API keys. Ever, for this course.
- Turn on Colab **T4 GPU**.
- Outputs from 0.5B–3B models will look rougher than ChatGPT. That is expected.
- Mini-project at the end of each week is the grade checkpoint; earlier labs are practice.

## Privacy

Local PC + Ollama never leaves the machine. Colab downloads public Hugging Face weights into Google’s VM; do not paste student PII into prompts.
