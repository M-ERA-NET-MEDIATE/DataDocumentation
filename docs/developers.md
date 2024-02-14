<!-- markdownlint-disable MD046 -->
# For developers and maintainers

## Tools

As part of the development environment, we use various tools or tooling:

- [pre-commit](https://pre-commit.com)
  As a versioned dependency in a `requirements.txt` file.
  With the hooks:
  - Check JSON
  - Check YAML
  - Fix end-of-file
  - Remove trailing whitespace
  - Run [markdownlint](https://github.com/DavidAnson/markdownlint-cli2), fixing files in-place, where possible.
  - Run [ci-cd](https://SINTEF.github.io/ci-cd)'s [_Update Landing Page (index.md) for Documentation_](https://SINTEF.github.io/ci-cd/latest/hooks/docs_landing_page) hook.
- [Dependabot](https://docs.github.com/en/code-security/dependabot)
  Update dependencies (currently only `pre-commit`) in `requirements.txt`.
  Update GitHub Actions used in CI/CD workflows.
- GitHub Actions CI/CD workflows
  - _CI - Activate auto-merging for automated PRs_
    Runs when a PR is opened by Dependabot or pre-commit.ci that targets the `main` branch.
- [pre-commit.ci](https://pre-commit.ci)
  Added through special configuration in the `.pre-commit-config.yaml` file.
  It does two things:
  - Run `pre-commit` for all PRs as a status check.
  - Automatically open PRs to update the `pre-commit` hooks.

## Setup development environment

To set up the development environment, first clone the repository into a local directory, enter it and then install the dependencies in the `requirements.txt` file.

```bash
git clone https://github.com/M-ERA-NET-MEDIATE/DataDocumentation.git
cd DataDocumentation
pip install -r requirements.txt
```

!!! note

    The clone URL is the HTTPS URL.
    If you have set up SSH keys for GitHub, you can use the SSH URL instead: `git@github.com:M-ERA-NET-MEDIATE/DataDocumentation.git`.

Run `pre-commit install` to ensure all hooks are run before each commit.

### Run `pre-commit` hooks

To run the hooks on all files, run `pre-commit run --all-files`.
