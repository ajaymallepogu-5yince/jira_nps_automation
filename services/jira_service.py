import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timezone
from config import JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json"
}


# -----------------------------
# GET ALL BOARDS (PAGINATION)
# -----------------------------
def get_all_boards():

    boards = []
    start_at = 0
    max_results = 50

    while True:

        url = f"{JIRA_BASE_URL}/rest/agile/1.0/board?startAt={start_at}&maxResults={max_results}"
        response = requests.get(url, headers=headers, auth=auth)
        data = response.json()
        values = data.get("values", [])
        boards.extend(values)

        if data.get("isLast", True):
            break

        start_at += max_results

    print(f"\nTotal boards found: {len(boards)}")
    return boards


# -----------------------------
# GET ACTIVE SPRINTS
# -----------------------------
def get_active_sprints(board_id):

    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint?state=active"
    response = requests.get(url, headers=headers, auth=auth)
    data = response.json()
    return data.get("values", [])


# -----------------------------
# GET SPRINT ISSUES
# -----------------------------
def get_sprint_issues(sprint_id):

    issues = []
    start_at = 0
    max_results = 50

    while True:

        url = f"{JIRA_BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue?startAt={start_at}&maxResults={max_results}"
        response = requests.get(url, headers=headers, auth=auth)
        data = response.json()
        batch = data.get("issues", [])
        issues.extend(batch)

        if start_at + max_results >= data.get("total", 0):
            break

        start_at += max_results

    return issues


# -----------------------------
# CHECK IF SPRINT ENDS TODAY
# -----------------------------
def sprint_ends_today(sprint):
    """
    Returns True if the sprint's endDate is today (in local date).
    Jira returns endDate in ISO 8601 format, e.g. "2025-03-06T23:59:00.000Z"
    """
    end_date_str = sprint.get("endDate")

    if not end_date_str:
        return False

    try:
        # Parse the ISO date string — handle both Z and +offset formats
        end_date_str_clean = end_date_str.replace("Z", "+00:00")
        end_dt = datetime.fromisoformat(end_date_str_clean)

        # Convert to local date for comparison
        end_date_local = end_dt.astimezone().date()
        today = datetime.now().date()

        return end_date_local == today

    except Exception as e:
        print(f"  [WARN] Could not parse sprint endDate '{end_date_str}': {e}")
        return False


# -----------------------------
# MAIN METRICS FUNCTION
# -----------------------------
def get_metrics():

    results = []
    boards = get_all_boards()

    for board in boards:

        board_id = board["id"]
        board_name = board["name"]

        print(f"\nChecking board: {board_name}")

        sprints = get_active_sprints(board_id)

        if not sprints:
            print("  No active sprint")
            continue

        for sprint in sprints:

            sprint_id = sprint["id"]
            sprint_name = sprint["name"]
            sprint_end = sprint.get("endDate", "N/A")

            print(f"  Active sprint: {sprint_name} | Ends: {sprint_end}")

            issues = get_sprint_issues(sprint_id)

            total = len(issues)
            done = 0
            bugs = 0
            story_points = 0

            for issue in issues:

                fields = issue["fields"]
                status = fields["status"]["name"].lower()
                issue_type = fields["issuetype"]["name"].lower()
                sp = fields.get("customfield_10016")

                if sp:
                    story_points += sp

                if "done" in status:
                    done += 1

                if issue_type == "bug":
                    bugs += 1

            results.append({
                "project_name": board_name,
                "sprint_name": sprint_name,
                "sprint_id": sprint_id,
                "sprint_end_date": sprint_end,
                "ends_today": sprint_ends_today(sprint),   # ← KEY FLAG
                "total_issues": total,
                "completed_issues": done,
                "bugs_fixed": bugs,
                "story_points": story_points
            })

    return results


# -----------------------------
# GET ONLY SPRINTS ENDING TODAY
# -----------------------------
def get_sprints_ending_today():
    """
    Convenience function: returns only the sprint metrics
    where the sprint ends today — used by main.py to trigger emails.
    """
    all_metrics = get_metrics()
    ending_today = [m for m in all_metrics if m.get("ends_today")]

    print(f"\nSprints ending today: {len(ending_today)}")
    return ending_today


# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":

    data = get_sprints_ending_today()

    print("\nFINAL RESULT (Sprints ending today):\n")
    for item in data:
        print(item)