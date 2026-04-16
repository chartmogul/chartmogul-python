#!/bin/bash
# PostToolUse (Edit|Write): record touched file for batch processing in Stop.
# Must be <50ms. No linting, no formatting, no git calls.
cd "$CLAUDE_PROJECT_DIR" || exit 0

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

[[ -z "$FILE" ]] && exit 0
[[ "$FILE" != *.py ]] && exit 0

# Skip generated/vendored paths
case "$FILE" in
  *__pycache__*|*.egg-info*|*/dist/*|*/build/*|*/node_modules/*|*/vendor/*|*/coverage/*) exit 0 ;;
esac

# Append to tracker (dedup at read time)
echo "$FILE" >> /tmp/claude-py-touched-files 2>/dev/null || true

exit 0
