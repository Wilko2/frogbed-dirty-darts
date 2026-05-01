#!/usr/bin/env python3
"""
create_milestone_branches.py

Optional helper for creating local milestone branches.

Recommended use:
    python scripts/create_milestone_branches.py --start 0 --end 16

Why only 0-16 first?
Because those milestones get you to the first playable terminal leg.
Creating all 52 branches at once can make GitHub visually confusing.
"""

from __future__ import annotations

import argparse
import re
import subprocess


MILESTONE_TITLES = {
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


def slugify(text: str) -> str:
    text = text.lower().replace("/", "").replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def branch_name(num: int) -> str:
    return f"milestone-{num:02d}-{slugify(MILESTONE_TITLES[num])}"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create local FrogBed milestone branches.")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=16)
    parser.add_argument("--push", action="store_true", help="Also push branches to origin.")
    args = parser.parse_args()

    for num in range(args.start, args.end + 1):
        if num not in MILESTONE_TITLES:
            print(f"Skipping unknown milestone {num}")
            continue

        b = branch_name(num)
        created = run(["git", "branch", b])

        if created.returncode == 0:
            print(f"created: {b}")
        else:
            print(f"not created: {b} ({created.stderr.strip() or created.stdout.strip()})")

        if args.push:
            pushed = run(["git", "push", "-u", "origin", b])
            if pushed.returncode == 0:
                print(f"pushed: {b}")
            else:
                print(f"not pushed: {b} ({pushed.stderr.strip() or pushed.stdout.strip()})")


if __name__ == "__main__":
    main()
