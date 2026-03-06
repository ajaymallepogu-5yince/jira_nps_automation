import json

from services.jira_service import get_sprints_ending_today
from services.summary_service import generate_summary
from services.email_service import send_email
from services.slack_service import send_slack_message


def load_clients():

    with open("data/clients.json") as f:
        return json.load(f)


def run():

    print("Checking for sprint completion...")

    clients = load_clients()

    sprints = get_sprints_ending_today()

    if not sprints:
        print("No sprint ended today")
        return

    for sprint in sprints:

        project = sprint["project_name"]
        sprint_name = sprint["sprint_name"]

        print(f"\nSprint ending today: [{project}] {sprint_name}")
        print(f"  Total Issues    : {sprint['total_issues']}")
        print(f"  Completed       : {sprint['completed_issues']}")
        print(f"  Bugs Fixed      : {sprint['bugs_fixed']}")
        print(f"  Story Points    : {sprint['story_points']}")

        client_email = clients.get(project)

        if not client_email:
            print(f"  [SKIP] No client email found for project: '{project}'")
            continue

        summary = generate_summary(sprint)

        send_email(
            client_email,
            f"Sprint Completed - {sprint_name}",
            summary
        )

        send_slack_message(summary)

        print(f"  [DONE] Email sent to {client_email} | Slack notified")


if __name__ == "__main__":

    run()