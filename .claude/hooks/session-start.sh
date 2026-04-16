#!/bin/bash
# SessionStart: detect repo state, warn about stale deps. Must be <1s, no network.
cd "$CLAUDE_PROJECT_DIR" || exit 0

context=""

# Check for uncommitted changes
dirty=$(git status --porcelain 2>/dev/null | head -5)
if [[ -n "$dirty" ]]; then
  count=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  context+="Uncommitted changes ($count files). "
fi

# Check current branch
branch=$(git branch --show-current 2>/dev/null)
if [[ -n "$branch" ]]; then
  context+="On branch: $branch. "
fi

# Check if deps are installed
if ! python -c "import chartmogul" 2>/dev/null; then
  context+="WARNING: chartmogul package not installed. Run: pip install -e .[testing]"
fi

# Reset file tracker for this session
: > /tmp/claude-py-touched-files 2>/dev/null || true

if [[ -n "$context" ]]; then
  jq -n --arg ctx "$context" \
    '{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": $ctx}}'
fi

exit 0
