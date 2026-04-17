# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced sales-oriented README with architecture diagram (mermaid), stack table, consulting CTA and author bio.
- `examples/basic_usage.py` — self-contained example showing init, insert with dedup, search, JSON export.
- `CONTRIBUTING.md` — contribution workflow and style guide.
- `CHANGELOG.md` — versioned change tracking.
- Issue templates (`bug_report.md`, `feature_request.md`).
- Pull request template.
- GitHub Actions workflow `ci.yml` — Python lint + smoke test on push and pull request.
- Repository topics: ai, automation, consulting, gabon, africa, intelligence, sqlite, python, monitoring, data-pipeline, osint.
- Expanded `.gitignore` entries for SQLite journals, IDE artifacts and local virtualenvs.

### Changed
- Repository description and homepage updated to reflect consulting positioning.

## [0.1.0] - 2026-03-27

### Added
- Initial release: Intelligence Monitoring Agent skeleton for Gabon.
- Four monitored sectors: Transport (Gabon), Transport (Africa), PNDT, Mining (Gabon).
- SQLite storage and SHA-256 based deduplication concept documented.
