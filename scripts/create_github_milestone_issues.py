#!/usr/bin/env python3
"""
create_github_milestone_issues.py

This script creates GitHub Issues for the FrogBed / Dirty Darts milestones.

What it does:
- Reads the milestone list below.
- Creates one GitHub Issue per milestone.
- Each issue points agents to:
  - AGENTS.md
  - docs/milestones/milestone_XX.md

Important:
- This script does NOT create branches.
- This script does NOT edit game code.
- It only creates online GitHub Issues/task cards.

Before using it:
1. Install GitHub CLI if you have not already.
2. Log in with:
   gh auth login

Run from the root of the repo:

    python scripts/create_github_milestone_issues.py

Create only first 16:

    python scripts/create_github_milestone_issues.py --start 0 --end 16

Test what it WOULD create without actually creating issues:

    python scripts/create_github_milestone_issues.py --dry-run
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


MILESTONES = {
    0: "Freeze the Project Spine",
    1: "Fix Import Structure",
    2: "Board Model",
    3: "Ring and Resolved Dart Validation",
    4: "Weight Profile Engine",
    5: "Future Dart Generator",
    6: "Manual Visit Input Model",
    7: "Candidate Generation",
    8: "First Play Detection",
    9: "Play Multiplier Table",
    10: "Mult Stacking",
    11: "Scoring Package Resolver",
    12: "Best Package Selection",
    13: "Visit Event Detection",
    14: "Full Visit Resolver",
    15: "Leg State Engine",
    16: "Terminal Leg Runner",
    17: "Dirty Dart Content Catalogue",
    18: "Dirty Dart Transformation Engine",
    19: "Dirty Dart Selection in Visit",
    20: "Character Signatures",
    21: "In-Turn State Design Lock",
    22: "State Model Code",
    23: "State Resolver",
    24: "Next-Visit Weight Modifiers from State",
    25: "Coaster Content Catalogue",
    26: "Coaster Trigger Engine",
    27: "Economy Layer",
    28: "Enemy Model",
    29: "Game Engine",
    30: "Bar Node Prototype",
    31: "Shop / Reward Draft",
    32: "Drinks, Set-Ups, Rituals Design Lock",
    33: "Drinks / Set-Ups / Rituals Code",
    34: "Moments Design Lock",
    35: "Moment Detection Code",
    36: "Meta Currency Stub",
    37: "Brewery Design Lock",
    38: "Brewery Tags in Content",
    39: "First Run Loop",
    40: "Save / Load Stub",
    41: "Simulation Harness",
    42: "Play Frequency Report",
    43: "Dirty Dart Balance Report",
    44: "Coaster Balance Report",
    45: "UI Boundary Lock",
    46: "Simple Text UI Polish",
    47: "Basic Visual Prototype Decision",
    48: "Dartboard Renderer Prototype",
    49: "First Playable Alpha Checklist",
    50: "Alpha Content Minimum",
    51: "Explicit Deferred List",
    52: "The Big Design Fork",
}


def make_issue_body(num: int, title: str) -> str:
    milestone_file = f"docs/milestones/milestone_{num:02d}.md"

    body = f"""## Milestone

Milestone {num:02d} — {title}

## What this issue is

This is a task card for one FrogBed / Dirty Darts milestone.

The agent or developer working on this issue should only work on this milestone.

## Source of truth

Read these files before doing any work:

- AGENTS.md
- {milestone_file}

## Before coding, state

1. Current milestone number
2. Dependencies
3. Files you will touch
4. Tests you will add or change
5. What is explicitly out of scope

## Required output

- [ ] Implement only this milestone
- [ ] Add or update tests if code changed
- [ ] Run python -m pytest
- [ ] Add manual check notes
- [ ] Do not implement later milestones
- [ ] Do not delete previous milestone work

## What "out of scope" means

Out of scope means: do not build later features early.

Example:
If this is Milestone 02 — Board Model, do not also build:
- future dart generation
- dirty darts
- coasters
- enemies
- UI

Those later features have their own milestone files.

## Branch instruction

When starting work, create a branch from the latest main branch.

Branch name should follow this style:

milestone-{num:02d}-{title.lower().replace(" ", "-").replace("/", "").replace("—", "-")}

## Completion rule

Do not close this issue until:
- the related code or design document exists
- tests pass, where relevant
- the work has been reviewed
"""
    return body


def run_command(command: list[str], dry_run: bool) -> None:
    print()
    print("COMMAND:")
    print(" ".join(command))

    if dry_run:
        print("DRY RUN: not creating issue.")
        return

    result = subprocess.run(command, text=True, capture_output=True)

    if result.returncode != 0:
        print("ERROR:")
        print(result.stderr.strip())
    else:
        print("SUCCESS:")
        print(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Create FrogBed milestone issues on GitHub.")
    parser.add_argument("--start", type=int, default=0, help="First milestone number to create.")
    parser.add_argument("--end", type=int, default=52, help="Last milestone number to create.")
    parser.add_argument("--dry-run", action="store_true", help="Preview commands without creating issues.")
    args = parser.parse_args()

    if not Path(".git").exists():
        raise SystemExit("ERROR: Run this from the root of your Git repo, where the .git folder exists.")

    for num in range(args.start, args.end + 1):
        if num not in MILESTONES:
            print(f"Skipping unknown milestone {num}")
            continue

        title = MILESTONES[num]
        issue_title = f"Milestone {num:02d} — {title}"
        issue_body = make_issue_body(num, title)

        command = [
            "gh",
            "issue",
            "create",
            "--title",
            issue_title,
            "--body",
            issue_body,
            "--label",
            "milestone",
            "--label",
            "frogbed",
        ]

        run_command(command, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
