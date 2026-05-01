# FrogBed / Dirty Darts Agent Rules

You are working on FrogBed / Dirty Darts.

## Non-negotiable rules

1. Never skip milestones.
2. Never delete or replace earlier milestone work.
3. Never rewrite architecture unless the issue explicitly asks for it.
4. Do not implement future milestone features early.
5. Every milestone must include:
   - code or design document, depending on milestone type
   - tests where code changes are made
   - manual check instructions
   - notes on what remains unsolved

## Before coding, state

- Current milestone number
- Dependencies
- Files you will touch
- Tests you will add/change
- What is explicitly out of scope

## Architecture boundaries

- `core/` = pure models, enums, IDs, board concepts
- `systems/` = runtime game logic
- `content/` = authored data/catalogues
- `sim/` = simulations/manual runners/reports
- `ui/` = display only
- `data/` = save/schema/data files
- `docs/` = design locks, milestone notes, decisions
- `.github/` = issue templates and GitHub workflow files

UI must not own game rules.

## Testing

Run:

```bash
python -m pytest
```

Do not claim completion if tests fail.

## FrogBed design guardrails

- FrogBed is the title/apex play, not the whole theme.
- Dirty Darts are cheating/toolbox darts.
- Future/Silver darts are natural offered darts.
- The player chooses darts; the game chooses the best outcome.
- Best 3 package model exists at least as the baseline.
- All 5 darts can feed events.
- Coasters are the main relic/build system.
- Breweries are flavour/content pools, not rigid classes.
- Pub/bar layer matters.
- Moments award meta currency/unlocks.
- Probability manipulation is central.
- Dartboard order stays fixed.
- Bosses manipulate scoring/probability/rules.
- Final boss is a corporate monopoly reveal, but should not be implemented early.
