# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Added
- `agents.py` with first agent "Moneypenny" wired to GPT-4o.
- `ui.pretty_print_response()` for green typewriter-style agent output.
- Modular `ui.py` to handle banners and console formatting.
- `sessions.py` to manage session logs and previews.

### Changed
- Refactored `flow.py` to delegate UI and agent calls to separate modules.
- Removed redundant `import ui` shadowing bug.
- Disabled enhanced transcript by default but kept code path available.
- Standardized user input echo: now always `User Selection: [n]`.

### Fixed
- Eliminated double echo bug on user selection.
- Fixed transcript logging to `.md` with clear sections.
- Prevented orphan imports from causing `UnboundLocalError`.

---
