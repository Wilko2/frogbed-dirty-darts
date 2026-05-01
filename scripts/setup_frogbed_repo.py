#!/usr/bin/env python3
"""
setup_frogbed_repo.py

Creates the FrogBed / Dirty Darts agentic project scaffold:

- core folders
- docs/milestones/milestone_00.md ... milestone_52.md
- AGENTS.md
- .github/ISSUE_TEMPLATE/milestone_task.md
- docs/branch_plan.md
- docs/agentic_workflow.md
- basic .gitignore
- optional branch creation with --create-branches

Run from the ROOT of your local GitHub repo:

    python scripts/setup_frogbed_repo.py

Useful options:

    python scripts/setup_frogbed_repo.py --overwrite
    python scripts/setup_frogbed_repo.py --create-branches --branch-start 0 --branch-end 16
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Milestone:
    number: int
    title: str
    goal: str
    key_files: tuple[str, ...] = ()
    must_include: tuple[str, ...] = ()
    out_of_scope: tuple[str, ...] = ()


MILESTONES: tuple[Milestone, ...] = (
    Milestone(
        0,
        "Freeze the Project Spine",
        "Protect the architecture before adding systems.",
        ("README.md", "constants.py", "core/enums.py", "core/models.py", "systems/", "content/", "ui/"),
        (
            "No UI imports inside core or systems.",
            "No game rules hidden inside content.",
            "Existing dataclasses are not randomly rewritten.",
            "Tests still pass.",
        ),
        ("Feature implementation", "visual UI work", "coasters", "dirty dart logic"),
    ),
    Milestone(
        1,
        "Fix Import Structure",
        "Make the package runnable cleanly.",
        ("pyproject.toml", "README.md", "tests/"),
        (
            "Decide package-vs-flat run style.",
            "Standardise imports.",
            "Ensure python -m pytest works from repo root.",
            "No path hacks.",
        ),
        ("Board model", "weighting", "play detection"),
    ),
    Milestone(
        2,
        "Board Model",
        "Implement the dartboard as a pure model.",
        ("core/board.py", "tests/test_board.py"),
        (
            "Standard dart order.",
            "Clockwise and anti-clockwise neighbours.",
            "Distance around board.",
            "Ring multiplier.",
            "Bull handling.",
            "Outer Bull = 25.",
            "Bullseye = 50.",
            "Prime and high-prime helpers.",
            "Hemisphere helpers.",
            "Score helper.",
        ),
        ("Weighting", "future dart generation", "play detection", "visit resolving"),
    ),
    Milestone(
        3,
        "Ring and Resolved Dart Validation",
        "Make sure every resolved dart has valid score logic.",
        ("core/models.py", "core/board.py", "tests/test_resolved_darts.py"),
        (
            "Validate ResolvedDart creation through helpers.",
            "Avoid duplicated score calculation.",
            "Add resolve_score(tile, ring) helper.",
            "Bulls cannot accidentally use double/triple rings.",
        ),
        ("Future dart generation", "play detection", "dirty darts"),
    ),
    Milestone(
        4,
        "Weight Profile Engine",
        "Create probability weighting without generating darts yet.",
        ("systems/weighting.py", "tests/test_weighting.py"),
        (
            "WeightProfile.",
            "Segment weights.",
            "Ring weights.",
            "Bull weights.",
            "Modifier layers.",
            "Add, multiply, and force modifiers.",
            "Renormalisation.",
            "Deterministic weighted choice.",
        ),
        ("Actually generating future darts", "coasters", "states"),
    ),
    Milestone(
        5,
        "Future Dart Generator",
        "Generate the five natural offered darts.",
        ("systems/future_darts.py", "tests/test_future_darts.py"),
        (
            "Generate 5 FutureDart objects.",
            "Each dart has offered index, tile, ring, score, source, and debug info.",
            "Uses WeightProfile rather than hardcoded random choices.",
        ),
        ("Dirty darts", "play detection", "visit resolving"),
    ),
    Milestone(
        6,
        "Manual Visit Input Model",
        "Allow the player or simulation to choose darts from offered darts.",
        ("systems/selection.py", "tests/test_selection.py"),
        (
            "Select by offered index.",
            "Preserve chosen order.",
            "Prevent invalid selections.",
            "Allow up to 5 darts.",
        ),
        ("Dirty dart selection", "package scoring"),
    ),
    Milestone(
        7,
        "Candidate Generation",
        "Generate all possible 3-dart scoring packages from chosen darts.",
        ("systems/candidates.py", "tests/test_candidates.py"),
        (
            "Input chosen resolved darts.",
            "Output all 3-dart combinations.",
            "For 5 darts, exactly 10 candidates are generated.",
            "Preserve candidate indices.",
            "Do not score candidates yet.",
        ),
        ("Play detection", "package scoring", "events"),
    ),
    Milestone(
        8,
        "First Play Detection",
        "Detect the first playable batch of patterns.",
        ("systems/play_detection.py", "tests/test_play_detection.py"),
        (
            "Run.",
            "Ladder.",
            "Three in a Bed.",
            "FrogBed.",
            "Prime Set.",
            "Same Ring.",
            "All Doubles.",
            "All Triples.",
            "Bull Pair.",
            "Hat Trick.",
        ),
        ("Golden Ratio", "Pierce", "Territory", "Orbit", "Sandwich", "Mirror"),
    ),
    Milestone(
        9,
        "Play Multiplier Table",
        "Create one source of truth for play values.",
        ("content/play_values.py", "tests/test_play_values.py"),
        (
            "Play detection does not own balance values.",
            "Values can be adjusted without rewriting logic.",
            "Include starter values for core alpha plays.",
        ),
        ("Scoring packages", "mult stacking"),
    ),
    Milestone(
        10,
        "Mult Stacking",
        "Score packages with multiple detected plays.",
        ("systems/mult_stack.py", "tests/test_mult_stack.py"),
        (
            "Implement Formula A for comparison.",
            "Implement Formula B for alpha default.",
            "Single play returns native mult.",
            "Two and three play packages stack deterministically.",
            "Highest mult play is treated as primary.",
        ),
        ("Candidate scoring", "visit resolving"),
    ),
    Milestone(
        11,
        "Scoring Package Resolver",
        "Turn candidates into scored packages.",
        ("systems/package_scoring.py", "tests/test_package_scoring.py"),
        (
            "Calculate base score.",
            "Detect plays.",
            "Calculate mult.",
            "Calculate final score.",
            "Produce human-readable explanation.",
        ),
        ("Best package selection", "events", "leg engine"),
    ),
    Milestone(
        12,
        "Best Package Selection",
        "Pick the best scoring package from all candidates.",
        ("systems/package_selection.py", "tests/test_package_selection.py"),
        (
            "Highest final score wins.",
            "Tie-break by number of plays.",
            "Tie-break by highest native play value.",
            "Tie-break by base score.",
            "Tie-break by earlier chosen darts.",
            "Debug mode can expose all candidates.",
        ),
        ("Events", "visit resolving", "coasters"),
    ),
    Milestone(
        13,
        "Visit Event Detection",
        "Detect events from all chosen darts, not just the best package.",
        ("systems/events.py", "tests/test_events.py"),
        (
            "RUN_ANYWHERE.",
            "LADDER_ANYWHERE.",
            "DOUBLES_ANYWHERE.",
            "TRIPLES_ANYWHERE.",
            "BULL_PAIR.",
            "HAT_TRICK.",
            "ALL_DIFFERENT.",
            "REPEAT_HIT.",
            "EVEN_COUNT.",
            "ODD_COUNT.",
        ),
        ("Coaster triggers", "states", "moments"),
    ),
    Milestone(
        14,
        "Full Visit Resolver",
        "Resolve a whole visit in one system.",
        ("systems/visit_resolver.py", "tests/test_visit_resolver.py"),
        (
            "Receive chosen darts.",
            "Generate candidates.",
            "Score candidates.",
            "Choose best package.",
            "Detect visit events.",
            "Create VisitResolution.",
            "Return explanations/debug notes.",
        ),
        ("Leg engine", "dirty darts", "coasters", "states"),
    ),
    Milestone(
        15,
        "Leg State Engine",
        "Apply visit scores to a countdown leg.",
        ("systems/leg_engine.py", "tests/test_leg_engine.py"),
        (
            "Start 101/301/501.",
            "Apply visit score.",
            "Update remaining score.",
            "Detect win.",
            "Simple alpha bust rule: below zero scores 0 and keeps previous remaining score.",
        ),
        ("Enemy model", "game engine", "shop"),
    ),
    Milestone(
        16,
        "Terminal Leg Runner",
        "Create the first playable terminal prototype.",
        ("sim/manual_leg_runner.py", "tests/test_manual_leg_runner_smoke.py"),
        (
            "Start a 101 leg.",
            "Show 5 future darts.",
            "Let player choose up to 5.",
            "Show best scoring package.",
            "Show events.",
            "Show remaining score.",
            "Continue until win/loss.",
        ),
        ("Dirty darts", "enemies", "coasters"),
    ),
    Milestone(
        17,
        "Dirty Dart Content Catalogue",
        "Add dirty darts as authored content.",
        ("content/dirty_darts.py", "tests/test_dirty_dart_content.py"),
        (
            "Drift.",
            "Mimic.",
            "Gambler.",
            "Bull Dart.",
            "Force Double.",
            "Force Triple.",
            "Alpha decision: dirty darts score after transformation.",
        ),
        ("Non-scoring dirty dart model", "state-heavy dirty model"),
    ),
    Milestone(
        18,
        "Dirty Dart Transformation Engine",
        "Dirty darts can alter darts before scoring.",
        ("systems/dirty_darts.py", "tests/test_dirty_darts.py"),
        (
            "Player selects dirty dart.",
            "Dirty dart chooses target.",
            "Transformation occurs.",
            "Result becomes ResolvedDart.",
            "Transformed flag is set.",
            "Explanation records why.",
        ),
        ("Dirty dart selection UI", "coasters"),
    ),
    Milestone(
        19,
        "Dirty Dart Selection in Visit",
        "Dirty darts enter actual play.",
        ("systems/selection.py", "systems/visit_resolver.py", "sim/manual_leg_runner.py", "tests/test_dirty_visit_selection.py"),
        (
            "Player can choose future darts.",
            "Player can choose dirty darts.",
            "Player can mix them in order.",
            "FrogBed attempt with Mimic/Force Triple is possible.",
        ),
        ("Non-scoring dirty dart model", "state engine"),
    ),
    Milestone(
        20,
        "Character Signatures",
        "Add character identity.",
        ("content/characters.py", "systems/signatures.py", "tests/test_signatures.py"),
        (
            "Drifter signature.",
            "Gambler signature.",
            "Mimic signature.",
            "Gammon signature.",
            "Player chooses one character at run start.",
        ),
        ("Full character progression", "classes", "skill tree"),
    ),
    Milestone(
        21,
        "In-Turn State Design Lock",
        "Define states before coding them.",
        ("docs/design/in_turn_states.md",),
        (
            "Define RUN.",
            "Define FROGBED PRESSURE.",
            "Define PARITY.",
            "Delay LADDER, TERRITORY, PRECISION for later.",
            "Written design file exists before code.",
        ),
        ("State code", "state resolver"),
    ),
    Milestone(
        22,
        "State Model Code",
        "Represent states cleanly.",
        ("core/states.py", "tests/test_states.py"),
        (
            "Active state name.",
            "Source play/event.",
            "Duration.",
            "In-turn modifier.",
            "Next-visit modifier.",
            "Explanation.",
            "States exist independently from coasters.",
        ),
        ("State resolver", "next-visit weighting"),
    ),
    Milestone(
        23,
        "State Resolver",
        "Turn events and plays into states.",
        ("systems/state_resolver.py", "tests/test_state_resolver.py"),
        (
            "Inspect package plays.",
            "Inspect visit events.",
            "Produce states.",
            "Apply state priority.",
            "Only one primary state per visit at first.",
            "Priority: FrogBed Pressure, Run, Parity.",
        ),
        ("Next-visit weight modifiers", "coaster reactions to states"),
    ),
    Milestone(
        24,
        "Next-Visit Weight Modifiers from State",
        "States affect future dart generation.",
        ("systems/weighting.py", "systems/future_darts.py", "systems/state_resolver.py", "tests/test_state_weight_modifiers.py"),
        (
            "RUN biases adjacent continuation tiles.",
            "FROGBED PRESSURE biases repeated tile/ring.",
            "PARITY_ODD biases odd tiles.",
            "PARITY_EVEN biases even tiles.",
            "State from Visit 1 can affect dart generation in Visit 2.",
        ),
        ("Coasters", "drinks", "rituals"),
    ),
    Milestone(
        25,
        "Coaster Content Catalogue",
        "Add build relics.",
        ("content/coasters.py", "tests/test_coaster_content.py"),
        (
            "At least 10 starter coasters.",
            "Coasters are data first, not hardcoded everywhere.",
            "Include Run Mat, Bed Stain, Prime Receipt, Triple Foam, Frog Sticker, Odd Ale Mat, Even Lager Mat, Bull Ring, Worn Oche, Sticky Table.",
        ),
        ("Coaster trigger engine", "full shop"),
    ),
    Milestone(
        26,
        "Coaster Trigger Engine",
        "Coasters react to visit outcomes.",
        ("systems/coasters.py", "tests/test_coasters.py"),
        (
            "Trigger from scoring package plays.",
            "Trigger from visit events.",
            "Trigger from dirty dart usage.",
            "Trigger from state gained.",
            "At least 5 coasters work in terminal.",
        ),
        ("Full reward economy", "brewery unlocks"),
    ),
    Milestone(
        27,
        "Economy Layer",
        "Money and rewards matter.",
        ("systems/economy.py", "tests/test_economy.py"),
        (
            "Earn money from visits.",
            "Earn money from coasters.",
            "Store run money.",
            "Prepare for spending later in bar.",
        ),
        ("Full shop pricing", "meta economy"),
    ),
    Milestone(
        28,
        "Enemy Model",
        "Add opponents.",
        ("core/enemies.py", "content/enemies.py", "systems/enemy_engine.py", "tests/test_enemies.py"),
        (
            "Pub Regular.",
            "Tile Suppressor.",
            "Ring Taxer.",
            "Probability Thief.",
            "Alpha starts with Pub Regular only.",
        ),
        ("Final boss", "full boss kits"),
    ),
    Milestone(
        29,
        "Game Engine",
        "Create a best-of-3 legs game against one enemy.",
        ("systems/game_engine.py", "tests/test_game_engine.py"),
        (
            "Create legs.",
            "Track player leg wins.",
            "Track enemy leg wins.",
            "Detect match win/loss.",
        ),
        ("Full run loop", "bar map"),
    ),
    Milestone(
        30,
        "Bar Node Prototype",
        "Create a basic between-fight layer.",
        ("systems/bar_engine.py", "content/bars.py", "tests/test_bar_engine.py"),
        (
            "Bar contains next fight.",
            "Bar contains shop/reward placeholder.",
            "Bar contains drink offer placeholder.",
            "After winning, choose 1 of 3 coasters and 1 dirty dart upgrade.",
        ),
        ("Full shop economy", "complex map"),
    ),
    Milestone(
        31,
        "Shop / Reward Draft",
        "Give the player build choices.",
        ("systems/rewards.py", "tests/test_rewards.py"),
        (
            "Coaster reward.",
            "Dirty Dart reward.",
            "Clip Size reward.",
            "Money reward.",
            "Drink reward.",
            "Ritual reward.",
            "Use post-fight reward choices first.",
        ),
        ("Full shop prices", "metanodes"),
    ),
    Milestone(
        32,
        "Drinks, Set-Ups, Rituals Design Lock",
        "Protect pub flavour before coding.",
        ("docs/design/drinks_setups_rituals.md",),
        (
            "Define Drink.",
            "Define Set-up.",
            "Define Ritual.",
            "Define difference from Coaster.",
            "Written design file exists before implementation.",
        ),
        ("Drink code", "ritual code"),
    ),
    Milestone(
        33,
        "Drinks / Set-Ups / Rituals Code",
        "Implement only a small alpha batch.",
        ("content/drinks.py", "content/rituals.py", "content/setups.py", "systems/drinks.py", "systems/rituals.py", "systems/setups.py", "tests/test_drinks_rituals_setups.py"),
        (
            "Bitter.",
            "Lager.",
            "Stout.",
            "House Shot.",
            "Table Ritual.",
        ),
        ("Full pub economy", "large drink catalogue"),
    ),
    Milestone(
        34,
        "Moments Design Lock",
        "Define famous and rare plays without coding too early.",
        ("docs/design/moments.md",),
        (
            "Define Famous Play moments.",
            "Define Shape moments.",
            "Define Finish moments.",
            "Define Chain moments.",
            "Define Humiliation moments.",
            "Track moments but do not build full meta tree yet.",
        ),
        ("Moment code", "full historical database"),
    ),
    Milestone(
        35,
        "Moment Detection Code",
        "Detect rare achievements.",
        ("systems/moments.py", "content/moments.py", "tests/test_moments.py"),
        (
            "First FrogBed.",
            "FrogBed Finish.",
            "Dirty Finish.",
            "Pub Myth.",
        ),
        ("Full meta tree", "famous historical play database"),
    ),
    Milestone(
        36,
        "Meta Currency Stub",
        "Prepare for progression without overbuilding.",
        ("systems/meta.py", "tests/test_meta.py"),
        (
            "Add meta currency result.",
            "Award from moments.",
            "Do not build full tree.",
        ),
        ("Full metaprogression",),
    ),
    Milestone(
        37,
        "Brewery Design Lock",
        "Preserve brewery flavour.",
        ("docs/design/breweries.md",),
        (
            "Precision.",
            "Control.",
            "Chaos.",
            "Doubles/Triples.",
            "Math/Scholar.",
            "Corporate.",
            "Breweries are coaster pools and enemy flavour, not classes.",
        ),
        ("Brewery code", "faction politics"),
    ),
    Milestone(
        38,
        "Brewery Tags in Content",
        "Let content belong to brewery families.",
        ("content/coasters.py", "content/enemies.py", "content/drinks.py", "tests/test_brewery_tags.py"),
        (
            "Content supports brewery tags.",
            "Player can still mix builds.",
            "Do not turn breweries into rigid classes.",
        ),
        ("Full faction mechanics", "corporate final boss"),
    ),
    Milestone(
        39,
        "First Run Loop",
        "Combine systems into a basic run.",
        ("systems/run_engine.py", "sim/manual_run_runner.py", "tests/test_run_engine.py"),
        (
            "Choose character.",
            "Start bar.",
            "Fight enemy.",
            "Win game.",
            "Choose reward.",
            "Fight second enemy.",
            "Reach mini-boss or end.",
        ),
        ("Save/load", "visual UI", "full tour map"),
    ),
    Milestone(
        40,
        "Save / Load Stub",
        "Preserve run state.",
        ("data/save_schema.py", "systems/save_load.py", "tests/test_save_load.py"),
        (
            "Save seed.",
            "Save character.",
            "Save owned dirty darts.",
            "Save owned coasters.",
            "Save money.",
            "Save current bar/enemy/score.",
            "Reload a run in terminal.",
        ),
        ("Versioned migrations", "cloud saves"),
    ),
    Milestone(
        41,
        "Simulation Harness",
        "Balance with data, not vibes.",
        ("sim/sim_visits.py", "sim/sim_legs.py", "sim/sim_builds.py", "tests/test_sim_smoke.py"),
        (
            "Average visit score.",
            "Low-value visit rate.",
            "Play frequency.",
            "FrogBed frequency.",
            "Dirty dart value.",
            "Coaster trigger rate.",
            "State trigger rate.",
            "Leg length.",
            "Win rate.",
        ),
        ("Balance changes without report",),
    ),
    Milestone(
        42,
        "Play Frequency Report",
        "Check whether plays are too common or too rare.",
        ("sim/reports/play_frequency_report.py",),
        (
            "Output frequency table.",
            "Include Run, Ladder, Prime, FrogBed.",
            "Balance changes should reference this report.",
        ),
        ("Dirty dart balance", "coaster balance"),
    ),
    Milestone(
        43,
        "Dirty Dart Balance Report",
        "Check whether dirty darts are too strong.",
        ("sim/reports/dirty_dart_balance_report.py",),
        (
            "Silver only policy.",
            "Dirty light policy.",
            "Dirty heavy policy.",
            "FrogBed chase policy.",
            "Run chase policy.",
            "Dirty darts should improve play without replacing future darts.",
        ),
        ("All 5 scoring model switch",),
    ),
    Milestone(
        44,
        "Coaster Balance Report",
        "Check build paths.",
        ("sim/reports/coaster_balance_report.py",),
        (
            "Run build.",
            "FrogBed build.",
            "Prime build.",
            "Bull build.",
            "Dirty build.",
            "Economy build.",
        ),
        ("Full balancing pass",),
    ),
    Milestone(
        45,
        "UI Boundary Lock",
        "Make sure UI does not own rules.",
        ("docs/design/ui_boundary.md",),
        (
            "UI can display darts, score, events, package result, explanations.",
            "UI cannot decide scoring, plays, events, coasters, enemy effects.",
        ),
        ("Visual renderer implementation",),
    ),
    Milestone(
        46,
        "Simple Text UI Polish",
        "Make terminal prototype readable.",
        ("ui/text_ui.py", "sim/manual_run_runner.py"),
        (
            "Clear offered dart list.",
            "Chosen dart log.",
            "Package explanation.",
            "Event list.",
            "Coaster triggers.",
            "Remaining score.",
            "Enemy status.",
        ),
        ("Graphical dartboard",),
    ),
    Milestone(
        47,
        "Basic Visual Prototype Decision",
        "Choose next UI route.",
        ("docs/design/visual_prototype_decision.md",),
        (
            "Compare terminal, HTML/JS, Godot, and Pygame.",
            "Recommendation can be recorded.",
            "Do not implement renderer yet unless explicitly chosen.",
        ),
        ("Renderer implementation",),
    ),
    Milestone(
        48,
        "Dartboard Renderer Prototype",
        "Display the board visually.",
        ("ui/", "docs/design/dartboard_renderer_notes.md"),
        (
            "Show 20 segments.",
            "Show rings.",
            "Show bulls.",
            "Show offered darts.",
            "Highlight selected darts.",
            "Highlight scoring package.",
        ),
        ("Full animation", "final art"),
    ),
    Milestone(
        49,
        "First Playable Alpha Checklist",
        "Verify alpha readiness.",
        ("docs/alpha_checklist.md",),
        (
            "Player can start run.",
            "Player can choose character.",
            "Player receives future darts.",
            "Player can use dirty darts.",
            "Game resolves best scoring package.",
            "Events trigger from all darts.",
            "Coasters trigger.",
            "Leg can be won.",
            "Enemy can be beaten.",
            "Reward choice appears.",
            "Second fight starts.",
            "Debug explanations are readable.",
            "Tests cover core systems.",
        ),
        ("New feature implementation unless needed to complete checklist",),
    ),
    Milestone(
        50,
        "Alpha Content Minimum",
        "Define minimum required alpha content.",
        ("docs/alpha_content_minimum.md",),
        (
            "Required plays listed.",
            "Required dirty darts listed.",
            "Required characters listed.",
            "At least 10 coasters.",
            "At least 3 enemies.",
            "At least 1 bar.",
            "At least 3 reward choices after fight.",
        ),
        ("Huge content expansion",),
    ),
    Milestone(
        51,
        "Explicit Deferred List",
        "Protect against premature overbuilding.",
        ("docs/deferred_features.md",),
        (
            "Full metaprogression tree deferred.",
            "Famous historical play database deferred.",
            "Full brewery faction politics deferred.",
            "Final corporate boss deferred.",
            "Full shop economy deferred.",
            "Complex non-scoring dirty darts deferred.",
            "All 5 darts scoring model deferred.",
            "Multiplayer deferred.",
            "Full art/UI deferred.",
            "Save file versioning deferred.",
        ),
        ("Implementing deferred features",),
    ),
    Milestone(
        52,
        "The Big Design Fork",
        "Compare scoring models after alpha.",
        ("docs/design/big_design_fork.md",),
        (
            "Model A: Best 3 Score, All 5 Event.",
            "Model B: First 3 Create State, All 5 Score.",
            "Model C: Dirty Darts Utility Only.",
            "Model D: Full State Visit Model.",
            "Do not switch away from Model A until Model A is playable and measured.",
        ),
        ("Switching scoring model before alpha is measured",),
    ),
)


AGENTS_MD = """# FrogBed / Dirty Darts Agent Rules

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
"""


ISSUE_TEMPLATE = """---
name: FrogBed Milestone Task
about: One locked milestone implementation
title: "Milestone XX — "
labels: milestone, frogbed
assignees: ''
---

## Milestone

Milestone XX — NAME

## Source of truth

Use:

- `docs/milestones/milestone_XX.md`
- `AGENTS.md`

## Dependencies

- [ ] Previous milestone complete, unless this is Milestone 00
- [ ] Tests currently passing

## Required output

- [ ] Code or design document implemented
- [ ] Tests added or updated where code changed
- [ ] Manual check written
- [ ] No future milestone scope added
- [ ] Existing roadmap not rewritten

## Explicitly out of scope

Do not implement later milestone features unless explicitly required.

## Agent instruction

Before coding, state:

1. current milestone number
2. dependencies
3. files touched
4. tests added/changed
5. out-of-scope items
"""


GITIGNORE = """# Python
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/
env/
*.egg-info/

# IDE/editor
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Local data
*.sqlite
*.db
.env
"""


WORKFLOW_MD = """# FrogBed Agentic Workflow

This repo is designed for milestone-by-milestone AI-assisted development.

## Mental model

- GitHub = online project home
- Git = change tracker
- Local repo = the copy on your computer
- Branch = safe alternate timeline for one milestone
- Issue = task card
- Pull Request = review before accepting
- AGENTS.md = rules for AI workers
- Tests = quality control

## Default loop

1. Check out `main`
2. Pull latest
3. Create a milestone branch
4. Create or assign the GitHub issue
5. Agent works only on that branch
6. Run tests
7. Open PR
8. Review against milestone file
9. Merge back to `main`

## Commands

```bash
git checkout main
git pull
git checkout -b milestone-02-board-model
python -m pytest
git add .
git commit -m "Milestone 02 - Board Model"
git push -u origin milestone-02-board-model
```

## Agent prompt template

```text
Implement Milestone XX only.

Read:
- AGENTS.md
- docs/milestones/milestone_XX.md

Before coding, state:
1. current milestone number
2. dependencies
3. files touched
4. tests added/changed
5. out-of-scope items

Do not implement later milestones.
Run python -m pytest.
Open a PR when complete.
```
"""


MILESTONE_TEMPLATE = """# Milestone {num:02d} — {title}

## Goal

{goal}

## Dependencies

- Previous milestone must be complete unless this is Milestone 00.
- `python -m pytest` must pass before starting.

## Expected files / areas

{key_files}

## Must include

{must_include}

## Explicitly out of scope

{out_of_scope}

## Agent pre-flight checklist

Before coding, state:

1. Current milestone number
2. Dependencies
3. Files you will touch
4. Tests you will add/change
5. What is explicitly out of scope

## Implementation tasks

- [ ] Read `AGENTS.md`
- [ ] Read this milestone file
- [ ] Implement only this milestone
- [ ] Add or update tests if code changed
- [ ] Run `python -m pytest`
- [ ] Add manual check instructions

## Acceptance criteria

- [ ] Code/design output exists for this milestone
- [ ] Tests pass, where applicable
- [ ] No later milestone features added
- [ ] No previous milestone behaviour deleted
- [ ] Manual check documented

## Manual check

Write exact commands and expected output here.

## Completion notes

- What changed:
- What remains unsolved:
- Risks:
"""


def slugify(text: str) -> str:
    text = text.lower()
    text = text.replace("/", "")
    text = text.replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def bullet_list(items: tuple[str, ...]) -> str:
    if not items:
        return "- None specified."
    return "\n".join(f"- `{x}`" if "/" in x or "." in x else f"- {x}" for x in items)


def write_file(path: Path, text: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        print(f"skip existing: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote: {path}")


def ensure_folder(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    print(f"folder: {path}")


def make_branch_name(m: Milestone) -> str:
    return f"milestone-{m.number:02d}-{slugify(m.title)}"


def create_branches(start: int, end: int) -> None:
    for m in MILESTONES:
        if start <= m.number <= end:
            branch = make_branch_name(m)
            result = subprocess.run(
                ["git", "branch", branch],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print(f"created branch: {branch}")
            else:
                message = result.stderr.strip() or result.stdout.strip()
                print(f"branch not created: {branch} ({message})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create FrogBed agentic repo scaffold.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing generated files.")
    parser.add_argument("--create-branches", action="store_true", help="Also create local git branches.")
    parser.add_argument("--branch-start", type=int, default=0, help="First milestone branch to create.")
    parser.add_argument("--branch-end", type=int, default=16, help="Last milestone branch to create.")
    args = parser.parse_args()

    root = Path.cwd()

    folders = [
        "core",
        "systems",
        "content",
        "sim",
        "ui",
        "data",
        "docs",
        "docs/milestones",
        "docs/design",
        "docs/reports",
        "scripts",
        "tests",
        ".github",
        ".github/ISSUE_TEMPLATE",
    ]

    for folder in folders:
        ensure_folder(root / folder)

    write_file(root / "AGENTS.md", AGENTS_MD, args.overwrite)
    write_file(root / ".github" / "ISSUE_TEMPLATE" / "milestone_task.md", ISSUE_TEMPLATE, args.overwrite)
    write_file(root / ".gitignore", GITIGNORE, args.overwrite)
    write_file(root / "docs" / "agentic_workflow.md", WORKFLOW_MD, args.overwrite)

    # Keep empty Python package folders trackable and import-friendly.
    for package_folder in ["core", "systems", "content", "sim", "ui", "data", "tests"]:
        init_path = root / package_folder / "__init__.py"
        write_file(init_path, "", args.overwrite)

    branch_lines = ["# FrogBed Branch Plan\n"]
    for m in MILESTONES:
        branch_lines.append(f"- Milestone {m.number:02d}: `{make_branch_name(m)}` — {m.title}")
    write_file(root / "docs" / "branch_plan.md", "\n".join(branch_lines) + "\n", args.overwrite)

    for m in MILESTONES:
        milestone_text = MILESTONE_TEMPLATE.format(
            num=m.number,
            title=m.title,
            goal=m.goal,
            key_files=bullet_list(m.key_files),
            must_include=bullet_list(m.must_include),
            out_of_scope=bullet_list(m.out_of_scope),
        )
        write_file(root / "docs" / "milestones" / f"milestone_{m.number:02d}.md", milestone_text, args.overwrite)

    if args.create_branches:
        create_branches(args.branch_start, args.branch_end)

    print("\nDone.")
    print("Next commands usually are:")
    print("  git status")
    print("  git add .")
    print('  git commit -m "Set up FrogBed agentic scaffold"')
    print("  git push")


if __name__ == "__main__":
    main()
