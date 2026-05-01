# FrogBed Agentic Workflow

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
