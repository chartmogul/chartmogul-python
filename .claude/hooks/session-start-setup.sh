#!/bin/bash
# SessionStart: generate session ID, detect repo state. Must be <1s, no network.
cd "$CLAUDE_PROJECT_DIR" || exit 0

# Generate a stable session ID and persist via CLAUDE_ENV_FILE
# so the edit tracker and stop hook share the same file path
SESSION_ID="$(date +%s)-$$"
if [[ -n "$CLAUDE_ENV_FILE" ]]; then
  echo "export CLAUDE_HOOK_SESSION_ID='$SESSION_ID'" >> "$CLAUDE_ENV_FILE"
fi

ctx=""

# Warn about uncommitted changes
dirty=$(git diff --name-only 2>/dev/null | head -5)
if [[ -n "$dirty" ]]; then
  ctx+="Uncommitted changes:\n$dirty\n"
fi

# Report current branch
branch=$(git branch --show-current 2>/dev/null)
if [[ -n "$branch" ]]; then
  ctx+="Branch: $branch\n"
fi

# Check if deps are installed
if ! python3 -c "import chartmogul" 2>/dev/null; then
  ctx+="WARNING: chartmogul package not installed. Run: pip install -e .[testing]\n"
fi

if [[ -n "$ctx" ]]; then
  jq -n --arg ctx "$ctx" '{
    "hookSpecificOutput": {
      "hookEventName": "SessionStart",
      "additionalContext": $ctx
    }
  }'
fi

exit 0
