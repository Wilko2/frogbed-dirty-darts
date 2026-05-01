from pathlib import Path


def test_expected_project_folders_exist():
    root = Path(__file__).resolve().parents[1]

    expected_folders = [
        "core",
        "systems",
        "content",
        "sim",
        "ui",
        "data",
        "docs",
        "tests",
    ]

    for folder in expected_folders:
        assert (root / folder).is_dir()