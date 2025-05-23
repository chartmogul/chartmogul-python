# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

[Keep a Changelog]: https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html

## [4.6.1] - 2025-05-19
- Fixed Tasks API schema issue
- Unify requirements in a single place
- Support for Python 3.13.

## [4.6.0] - 2025-04-25
- Adds support for Tasks (https://dev.chartmogul.com/reference/tasks)

## [4.5.1] - 2025-04-07
- Update urllib3 dependency to use >=2.2.3 to allow for future minor updates

## [4.5.0] - 2025-03-18
- Adds support for disconnecting subscriptions
- Adds support for transaction fees to transactions

## [4.4.0] - 2024-10-24
- Adds support for unmerging customers

## [4.3.2] - 2024-06-26
- Remove VCR dependencies
- Replaced unit tests that depended on VCR using `request_mock`
- Updated urllib3 to latest secure version

## [4.3.1] - 2024-06-20
- Update the urllib3 dependency to a secure version

## [4.3.0] - 2024-03-25
- Adds support for Opportunities (https://dev.chartmogul.com/reference/opportunities)

## [4.2.1] - 2024-01-15
- Fix customer website_url, add missing allow_none=True

## [4.2.0] - 2024-01-08
- Add support for customer website_url

## [4.1.1] - 2023-12-21
- Fix missing customer_uuid when creating a note from a customer

## [4.1.0] - 2023-12-20
- Support customer notes

## [4.0.0] - 2023-10-04

### Added
- v4.0.0 upgrade instructions.
- Support for Python 3.12.

### Removed
- Support for old pagination using `page` query params.
- Deprecated `imp` module.
- Support for Python 3.7.

## [3.1.3] - 2023-09-27

### Added
- Support for cursor based pagination to `.all()` endpoints.
- Changelog.
