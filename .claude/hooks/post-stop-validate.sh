#!/bin/bash
# Stop: batch-lint files touched this turn, run test suite.
# Python has no autoformatter configured, so lint + tests only.
# Test suite runs in ~0.13s so it fits within the Stop budget.
cd "$CLAUDE_PROJECT_DIR" || exit 0

TRACKER="/tmp/claude-py-touched-files"
[[ ! -f "$TRACKER" ]] && exit 0

# Dedup file list, filter to files that still exist
files=()
while IFS= read -r f; do
  [[ -f "$f" ]] && files+=("$f")
done < <(sort -u "$TRACKER")

# Clear tracker for next turn
: > "$TRACKER" 2>/dev/null || true

[[ ${#files[@]} -eq 0 ]] && exit 0

# Lint only the touched files
output=$(python3 -m flake8 "${files[@]}" 2>&1) || true

# Run test suite (~0.13s)
test_output=$(python3 -m unittest 2>&1)
test_rc=$?
if [[ $test_rc -ne 0 ]]; then
  test_failures=$(echo "$test_output" | tail -20)
  output+=$'\n'"TEST FAILURES:\n$test_failures"
fi

if [[ -n "$output" ]]; then
  # Truncate to keep context short
  truncated=$(echo "$output" | head -20)
  total=$(echo "$output" | wc -l | tr -d ' ')
  if [[ "$total" -gt 20 ]]; then
    truncated+=$'\n'"... ($total total lint issues, showing first 20)"
  fi
  jq -n --arg ctx "$truncated" \
    '{"hookSpecificOutput": {"hookEventName": "Stop", "additionalContext": $ctx}}'
fi

exit 0
