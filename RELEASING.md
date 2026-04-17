# Releasing chartmogul-python

## Prerequisites

- You must have push access to the repository
- `git`, `gh`, `jq`, and `python3` must be installed
- Tags matching `v*` are protected by GitHub tag protection rulesets
- Releases are immutable once published (GitHub repository setting)
- PyPI [trusted publishing](https://docs.pypi.org/trusted-publishers/) must be configured for the package (see [Repository Settings](#repository-settings-admin))

## Release Process

Run the release script from the repository root:

```sh
bin/release.sh <patch|minor|major>
```

The script will:

1. Verify prerequisites and that CI is green on `main`
2. Show any open PRs targeting `main` and ask for confirmation
3. Show PRs merged since the last tag (what's being released) and ask for confirmation
4. Bump the version in `chartmogul/version.py`
5. Create a release branch, commit, push, and open a PR
6. Wait for the PR to be merged (poll every 10s)
7. Tag the merge commit and push the tag
8. Wait for the [release workflow](.github/workflows/release.yml) to complete, which will:
   - Run lint and the full test suite across Python 3.10-3.14
   - Verify that `chartmogul/version.py` version matches the tag
   - Build sdist and wheel
   - Create a GitHub Release with auto-generated release notes and attached distribution files
   - Publish to PyPI via [OIDC trusted publishing](https://docs.pypi.org/trusted-publishers/) with [build attestations](https://docs.pypi.org/attestations/)
9. Print links to the GitHub Release and PyPI package

## Changelog

Release notes are auto-generated from merged PR titles by the [release workflow](.github/workflows/release.yml). To ensure useful changelogs:

- Use clear, descriptive PR titles (e.g., "Add External ID field to Contact model")
- Prefix breaking changes with `BREAKING:` so they stand out in release notes
- After the release is created, review and edit the notes on the [Releases page](https://github.com/chartmogul/chartmogul-python/releases) if needed

## Pre-release Versions

For pre-release versions, use a semver pre-release suffix:

```sh
git tag v4.X.Y-rc1
git push origin v4.X.Y-rc1
```

These will be automatically marked as pre-releases on GitHub.

## Security

### Repository Protections

- **Immutable releases**: Once a GitHub Release is published, its tag cannot be moved or deleted, and release assets cannot be modified
- **Tag protection rulesets**: `v*` tags cannot be deleted or force-pushed

### PyPI

- Publishing uses [OIDC trusted publishing](https://docs.pypi.org/trusted-publishers/) — no long-lived API tokens are stored in the repository. GitHub Actions authenticates directly with PyPI via short-lived OIDC tokens.
- Once a package version is published to PyPI, [it cannot be republished](https://pypi.org/help/#file-name-reuse) with different contents
- Packages are published with [build attestations](https://docs.pypi.org/attestations/) (SLSA provenance), linking each version to the specific GitHub Actions run that built it
- Users can verify package integrity using pip's hash-checking mode (`--require-hashes`)
- Pinning versions in `requirements.txt` with hashes ensures reproducible installs

### What This Protects Against

- A compromised maintainer account cannot modify or delete existing releases
- No long-lived API tokens exist that could be leaked or stolen
- Tags cannot be moved to point to different commits after publication
- The PyPI registry provides an independent immutability layer beyond GitHub
- Build attestations allow anyone to verify a package was built from this repository by GitHub Actions

### Repository Settings (Admin)

These settings must be configured by a repository admin:

1. **Immutable Releases**: Settings > General > Releases > Enable "Immutable releases"
2. **Tag Protection Ruleset**: Settings > Rules > Rulesets > New ruleset targeting tags matching `v*` with deletion, force-push, and update prevention
3. **GitHub Actions Environment**: Settings > Environments > New environment named `pypi`
4. **PyPI Trusted Publishing**: On pypi.org, go to [chartmogul settings](https://pypi.org/manage/project/chartmogul/settings/publishing/) and configure a trusted publisher with: repository `chartmogul/chartmogul-python`, workflow `release.yml`, environment `pypi`
