# Releasing chartmogul-python

## Prerequisites

- You must have push access to the repository
- Tags matching `v*` are protected by GitHub tag protection rulesets
- Releases are immutable once published (GitHub repository setting)

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
6. The [release workflow](.github/workflows/release.yml) will automatically create a GitHub Release with auto-generated release notes
7. Verify the release appears at https://github.com/chartmogul/chartmogul-python/releases
8. Build and publish to PyPI:
   ```sh
   python3 setup.py sdist
   twine upload dist/*
   ```

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

- [PyPI](https://pypi.org) enforces version immutability: once a package version is published, it cannot be overwritten
- Users can verify package integrity using pip's hash-checking mode (`--require-hashes`)
- Pinning versions in `requirements.txt` with hashes ensures reproducible installs

### What This Protects Against

- A compromised maintainer account cannot modify or delete existing releases
- Tags cannot be moved to point to different commits after publication
- PyPI version immutability provides an independent verification layer beyond GitHub

### Repository Settings (Admin)

These settings must be configured by a repository admin:

1. **Immutable Releases**: Settings > General > Releases > Enable "Immutable releases"
2. **Tag Protection Ruleset**: Settings > Rules > Rulesets > New ruleset targeting tags matching `v*` with deletion and force-push prevention
