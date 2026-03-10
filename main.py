import json

from services.jira_service import get_sprints_ending_today
from services.summary_service import generate_summary
from services.email_service import send_email
from services.slack_service import send_sprint_notification
from services.log_service import log_email, already_sent_today, get_clients


def run():

    print("Checking for sprint completion...")

    # ── Load clients from Supabase DB (replaces clients.json) ───
    clients = get_clients()

    sprints = get_sprints_ending_today()

    if not sprints:
        print("No sprint ended today")
        return

    for sprint in sprints:

        project     = sprint["project_name"]
        sprint_name = sprint["sprint_name"]
        sprint_id   = sprint["sprint_id"]

        print(f"\nSprint ending today: [{project}] {sprint_name}")
        print(f"  Total Issues    : {sprint['total_issues']}")
        print(f"  Completed       : {sprint['completed_issues']}")
        print(f"  Bugs Fixed      : {sprint['bugs_fixed']}")
        print(f"  Story Points    : {sprint['story_points']}")

        # ── Duplicate guard ─────────────────────────────────────
        if already_sent_today(sprint_id):
            print(f"  [SKIP] Email already sent today for sprint_id={sprint_id}")
            continue

        # ── Client lookup ────────────────────────────────────────
        client_emails = clients.get(project)

        if not client_emails:
            print(f"  [SKIP] No client email found for project: '{project}'")
            continue

        # Normalize — always work as a list
        if isinstance(client_emails, str):
            client_emails = [client_emails]

        # ── Send email ───────────────────────────────────────────
        summary = generate_summary(sprint)

        try:
            send_email(
                client_emails,
                "BOS: NPS Survey",  # ← changed
                summary
            )
            email_status = "sent"
            print(f"  [EMAIL] Sent to {', '.join(client_emails)} ✅")

        except Exception as e:
            email_status = "failed"
            print(f"  [EMAIL] Failed → {e}")

        # ── Log to DB ────────────────────────────────────────────
        log_email(sprint, ", ".join(client_emails), status=email_status)

        # ── Slack notification ───────────────────────────────────
        if email_status == "sent":
            send_sprint_notification(project, sprint_name, ", ".join(client_emails), sprint)

        print(f"  [DONE] {project} / {sprint_name}")


if __name__ == "__main__":

    run()