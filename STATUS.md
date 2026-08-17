# STATUS — evals — 2026-08-17

## Now
Learning pydantic-evals. Harness is wired end-to-end but **has never been run**.

Next actions:
1. Run it: `uv run python -m evals.simple_eval_evaluator` — expect ~5-15s (spawns
   `claude -p` subprocess per case). Confirm the report table prints.
2. Wrap the run call in `if __name__ == '__main__':`
   (`src/evals/simple_eval_evaluator.py:27-28`) — currently top-level, so importing
   the module fires the whole eval as a side effect.
3. Add more cases to `src/evals/simple_eval_dataset.py` once one case passes.

## State
- 3 modules, all importable: `simple_eval_dataset.py` (1 Case), `simple_agent.py`
  (task fn `guess_city`), `simple_eval_evaluator.py` (2 evaluators + run call).
- Task fn shells out to `claude -p` rather than an API key / pydantic-ai Agent.
- No tests. No commits — repo is git-init'd but **zero commits**, everything untracked.
- `pydantic-evals` added to deps this session (was missing; only `pydantic-ai` was listed).

## Decisions this session
- Task fn lives in its own module (`simple_agent.py`), not beside the evaluators —
  keeps app code separate from test code so models can be swapped without touching evals.
- Task fn uses `claude -p` subprocess instead of an API key — reuses the CLI sub,
  no key management. Cost: full CLI boot per case, so this won't scale past ~tens of cases.
- Zed formats Python on save via ruff (`organizeImports` + `fixAll`), ruff + pyright
  both as language servers.

## Gotchas
- **`protect-paths.sh` now guards Bash too.** It was `Edit|Write|NotebookEdit` only;
  I wrote to Zed's settings.json via Bash, which walked around the block. Gap closed
  this session — matcher is now `Edit|Write|NotebookEdit|Bash` and the script scans
  command strings. It is deliberately conservative and **blocks reads**: any command
  merely containing `credentials`, `.env`, `/prod`, `client_secret`, `LaunchAgents`,
  or a non-`~/.claude` `settings.json` is denied. It blocked its own test script.
  Test suite: `python3 /tmp/hooktest.py` (9/9 passing; /tmp, so it won't survive reboot).
- Zed autosave is 1000ms + format-on-save is on — code may reformat mid-typing.
  Drop `autosave` in `~/.config/zed/settings.json` if that gets annoying.
- Pyright flags `@override` and dead `isinstance` checks in evaluators; these are
  style-level, not bugs.
- `EvaluatorContext.expected_output` is `str | None` — always None-guard before
  `.lower()`.

## Pointers
- `src/evals/simple_eval_evaluator.py:27` — top-level run call, needs `__main__` guard.
- `src/evals/simple_agent.py:5` — `claude -p` subprocess; add `--model` to pin, or
  `--output-format json` for token/cost data (then `json.loads(out)['result']`).
- `src/evals/simple_eval_dataset.py:10` — dataset, currently 1 case.
- `~/.claude/hooks/protect-paths.sh` — path guard, Bash branch at line ~91.
- `~/.claude/settings.json` — hook matcher registration.
- Docs example this is modelled on scores 1.00 with a hardcoded task fn; a green
  report only means the wiring works, not that the model is right.
