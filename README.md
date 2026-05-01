# FrogBed / Dirty Darts

FrogBed / Dirty Darts is a darts roguelike project built milestone-by-milestone.

## Development workflow

This repo uses an agentic milestone workflow:

- `AGENTS.md` contains rules for AI/developer agents.
- `docs/milestones/` contains the milestone source-of-truth files.
- GitHub Issues are task cards for each milestone.
- Branches are created one milestone at a time from the latest `main`.
- Pull Requests are used to review and merge milestone work.

## Architecture boundaries

- `core/` = pure models, enums, IDs, board concepts
- `systems/` = runtime game logic
- `content/` = authored data/catalogues
- `sim/` = simulations/manual runners/reports
- `ui/` = display only
- `data/` = save/schema/data files
- `docs/` = design locks, milestone notes, decisions

UI must not own game rules.

## Current status

The project scaffold is created. No gameplay systems are implemented yet.
