# Claude Code Instructions

Before drafting, revising, summarizing, or polishing prose in this repository,
read and follow:

`./.claude/skills/general-writing/SKILL.md`

Project-specific research and coding rules remain in:

`./AGENTS.md`

For the master thesis proposal, always follow the ZJU formatting authority:

`./08_admin/proposal_defense/zju_thesis_formatting_guidelines.md`

## Git Workflow

Git is plumbing here. The owner works on content and should never have to think
about branches or commits.

- Work directly on `main`. Do not create branches, worktrees, or PRs, and do not
  ask which branch to use.
- Commit each finished piece of work on `main` with a short, plain message, then
  `git push`. Run `git pull --ff-only` at the start of a session.
- Leave the repo clean at the end of every task: `git status` empty, `main`
  equal to `origin/main`, no stray branches, stashes, or worktrees.
- The repo is **public**. Never commit API keys, `.env` files, raw or processed
  data, literature PDFs, compiled PDFs, submitted files, or third-party
  documents (e.g. the Yanne reference proposal and slides in `07_misc/`). These
  are already covered by `.gitignore`; do not force-add them.
- Never rewrite history or force-push unless the owner asks for it.

## Where Things Are

- Active proposal source: `05_draft/proposal/main.tex` (compile with Tectonic).
- Submitted proposal PDF (local only):
  `06_output/submitted/2026-07-04_proposal_revised_final.pdf`.
- Current plan: `NEXT_STEPS.md` and `01_notes/Post-Defense Thesis Plan.md`.
- Reference proposal and defense slides from Yanne (local only): `07_misc/`.
