#!/bin/bash
# PostToolUse (Edit|Write|MultiEdit): record touched file for batch processing in Stop.
# Must be <50ms. No linting, no formatting, no git calls.
cd "$CLAUDE_PROJECT_DIR" || exit 0

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only track .py files, skip vendored/generated paths
if [[ "$FILE" == *.py ]] && [[ "$FILE" != *__pycache__* ]] && [[ "$FILE" != *.egg-info* ]] && [[ "$FILE" != */dist/* ]] && [[ "$FILE" != */build/* ]]; then
  TRACKER="/tmp/claude-edited-py-files-${CLAUDE_HOOK_SESSION_ID:-default}"
  echo "$FILE" >> "$TRACKER"
  sort -u "$TRACKER" -o "$TRACKER"
fi

exit 0
