"""Inject the evening policy; never classify prompts or call Notion here."""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9), "Asia/Tokyo")
POLICY = Path(__file__).resolve().parents[2] / "policies" / "evening-exploration.md"


def build_output(now, policy_path=POLICY):
    local = now.astimezone(JST)
    active = local.hour >= 19 or local.hour < 5
    context = (
        f"EVENING_EXPLORATION_GATE={'ACTIVE' if active else 'INACTIVE'}\n"
        f"Current time in Asia/Tokyo: {local.isoformat(timespec='minutes')}\n"
        "This gate state applies only to the current user turn and supersedes "
        "earlier evening gate states.\n"
    )
    if active:
        policy = policy_path.read_text(encoding="utf-8").strip()
        if not policy:
            raise ValueError("Evening policy is empty")
        context += "\n" + policy
    else:
        context += "The evening exploration policy is not active for this turn."
    return {"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit", "additionalContext": context,
    }}


def main():
    try:
        event = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
        if not isinstance(event, dict) or event.get("hook_event_name") != "UserPromptSubmit":
            raise ValueError("Expected a UserPromptSubmit event")
        output = build_output(datetime.now(JST))
    except (ValueError, OSError, UnicodeError) as error:
        # A broken installation must be visible, not silently disable the gate.
        # Do not print prompt contents or reflect them into developer context.
        print("Evening exploration hook failed: " + type(error).__name__, file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
