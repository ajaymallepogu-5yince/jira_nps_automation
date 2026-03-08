import requests
from config import SLACK_WEBHOOK_URL


def send_slack_message(message):
    """Raw text message — kept for backward compatibility."""

    if not SLACK_WEBHOOK_URL:
        print("  [SKIP] SLACK_WEBHOOK_URL not configured, skipping Slack notification")
        return

    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload)


def send_sprint_notification(project_name, sprint_name, client_email, sprint):
    """
    Sends a structured Slack notification when a sprint ends
    and an NPS feedback email has been dispatched to the client.

    Example message:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🏁 Sprint Ended Today
    Project  : INVStudio-StrongPosition
    Sprint   : INS - Sprint 12
    Client   : kalpana@bosframework.com  ← got the NPS email
    ─────────────────────────────
    📊 Sprint Metrics
    Total Issues   : 8
    Completed      : 0  (0%)
    Bugs Fixed     : 0
    Story Points   : 0
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """

    if not SLACK_WEBHOOK_URL:
        print("  [SKIP] SLACK_WEBHOOK_URL not configured, skipping Slack notification")
        return

    total     = sprint.get("total_issues",     0)
    completed = sprint.get("completed_issues", 0)
    bugs      = sprint.get("bugs_fixed",       0)
    points    = sprint.get("story_points",     0)

    completion_rate = round((completed / total) * 100) if total > 0 else 0

    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏁 *Sprint Ended Today*\n"
        f"*Project*  : {project_name}\n"
        f"*Sprint*   : {sprint_name}\n"
        f"*Client*   : {client_email}  ✅ NPS feedback email sent\n"
        f"─────────────────────────────\n"
        f"📊 *Sprint Metrics*\n"
        f"Total Issues   : {total}\n"
        f"Completed      : {completed}  ({completion_rate}%)\n"
        f"Bugs Fixed     : {bugs}\n"
        f"Story Points   : {points}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    payload = {"text": text}

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print(f"  [SLACK] Notification sent ✅")
        else:
            print(f"  [SLACK] Failed — HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"  [SLACK] Error: {e}")