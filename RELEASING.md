# Releasing chartmogul-python

## Prerequisites

- You must have push access to the repository
- Tags matching `v*` are protected by GitHub tag protection rulesets
- Releases are immutable once published (GitHub repository setting)
- PyPI Trusted Publisher must be configured (see [Setup](#trusted-publisher-setup-one-time) below)

## Release Process

1. Ensure all changes are merged to the `main` branch
2. Ensure CI is green on the `main` branch
3. Update the version in `chartmogul/version.py`
4. Commit the version bump
5. Create and push a version tag:
   ```sh
   git tag v4.X.Y
   git push origin v4.X.Y
   ```
6. The [release workflow](.github/workflows/release.yml) automatically:
   - Runs lint and tests across Python 3.10-3.14
   - Verifies the tag version matches `chartmogul/version.py`
   - Builds sdist and wheel
   - Publishes to PyPI via Trusted Publisher (OIDC)
   - Creates a GitHub Release with auto-generated notes and attached distribution files
7. Verify the release:
   - GitHub: https://github.com/chartmogul/chartmogul-python/releases
   - PyPI: https://pypi.org/project/chartmogul/

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

- Publishing uses [Trusted Publishers (OIDC)](https://docs.pypi.org/trusted-publishers/) — no API tokens or secrets are stored in the repository
- Authentication is based on GitHub's OIDC identity token, scoped to this specific repository, workflow file, and environment
- Each release includes [build attestations](https://docs.pypi.org/attestations/) (SLSA provenance), allowing users to cryptographically verify that the package was built from this repository
- [PyPI](https://pypi.org) enforces version immutability: once a package version is published, it cannot be overwritten
- Users can verify package integrity using pip's hash-checking mode (`--require-hashes`)
- Pinning versions in `requirements.txt` with hashes ensures reproducible installs

### What This Protects Against

- A compromised maintainer account cannot modify or delete existing releases
- Tags cannot be moved to point to different commits after publication
- No long-lived API tokens that could be leaked or stolen
- PyPI version immutability provides an independent verification layer beyond GitHub

### Repository Settings (Admin)

These settings must be configured by a repository admin:

1. **Immutable Releases**: Settings > General > Releases > Enable "Immutable releases"
2. **Tag Protection Ruleset**: Settings > Rules > Rulesets > New ruleset targeting tags matching `v*` with deletion and force-push prevention

### Trusted Publisher Setup (One-Time)

**On PyPI** (project maintainer):
1. Go to https://pypi.org/manage/project/chartmogul/settings/publishing/
2. Under "Add a new publisher", select "GitHub Actions"
3. Fill in: Owner = `chartmogul`, Repository = `chartmogul-python`, Workflow name = `release.yml`, Environment name = `pypi`
4. Click "Add"

**On GitHub** (repository admin):
1. Go to repository Settings > Environments
2. Create environment named `pypi`
3. Optionally add deployment protection rules (e.g., require approval from specific reviewers before publishing)
