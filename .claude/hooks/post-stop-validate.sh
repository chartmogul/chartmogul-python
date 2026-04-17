#!/bin/bash
# Stop: batch-lint touched files, run test suite (~0.13s).
# Python has no autoformatter configured, so lint + tests only.
cd "$CLAUDE_PROJECT_DIR" || exit 0

TRACKER="$CLAUDE_PROJECT_DIR/.claude/tmp/edited-py-files-${CLAUDE_HOOK_SESSION_ID:-default}"

ctx=""

# Batch flake8 on tracked files (if any were edited)
if [[ -f "$TRACKER" ]]; then
  files=$(cat "$TRACKER")
  rm -f "$TRACKER"

  if [[ -n "$files" ]]; then
    lint_out=$(echo "$files" | xargs python3 -m flake8 2>&1) || true
    offenses=$(echo "$lint_out" | grep -E "^.+:[0-9]+:[0-9]+:" | head -20)
    if [[ -n "$offenses" ]]; then
      ctx+="flake8 offenses:\n$offenses\n"
    fi
  fi
fi

# Always run tests - edits to tests or source both matter (~0.13s)
test_out=$(python3 -m unittest 2>&1)
test_exit=$?
if [[ $test_exit -ne 0 ]]; then
  summary=$(echo "$test_out" | grep -E "^(FAILED|ERROR)" | tail -1)
  failures=$(echo "$test_out" | grep -E "^(FAIL|ERROR):" | head -10)
  ctx+="tests failed ($summary):\n$failures\n"
fi

if [[ -n "$ctx" ]]; then
  jq -n --arg ctx "$ctx" '{
    "hookSpecificOutput": {
      "hookEventName": "Stop",
      "additionalContext": $ctx
    }
  }'
fi

exit 0
