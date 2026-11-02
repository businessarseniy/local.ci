# Contributing guide

This project follows simple git workflow.
- `master` branch for stable release
- `dev` branch for testing features and fixes
- `<scope>/<name>` branches for some work

## Working on feature/fix

Example will go for feature, but fix or other scopes follow
the same path

```bash
# On branch `dev`
git switch --create feature/my-feature-name
# Do your work with multiple commits
git push <remote-name> feature/my-feature-name
```

Then create pull request onto `dev` branch. This will do the testing
(actually TODO for now), and on all passed tests + review will be merged.

## Release

Will work via pull request `dev` branch onto `master` branch. Need to consider
some integration tests and approve only on everything OK.

## Extra

There are no linting/styling guides yet, but be sure not to pollute codebase
with some weird stuff (e.g. base64 encoded magic strings with unhelpful usage)
