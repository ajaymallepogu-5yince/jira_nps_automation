import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from config import JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json"
}

# ─────────────────────────────────────────────────────────
# CONTROLS
#
# TEST_MODE = True  → also picks up sprints that ended in
#                     the last TEST_DAYS_BACK days so you
#                     can test with REAL Jira data
# TEST_MODE = False → only today's sprints (PRODUCTION)
#
# MAX_SPRINTS       → max sprints to process per run
#
# USE_FAKE_AS_FALLBACK → if no real sprint found at all,
#                        use fake data below
#
# ── TO GO LIVE ───────────────────────────────────────────
# Set TEST_MODE            = False
# Set USE_FAKE_AS_FALLBACK = False
# ─────────────────────────────────────────────────────────
TEST_MODE            = True
TEST_DAYS_BACK       = 5
MAX_SPRINTS          = 2
USE_FAKE_AS_FALLBACK = True

FAKE_SPRINT = {
    # ── original fields ──────────────────────────────────
    "project_name":     "INVStudio-StrongPosition",
    "sprint_name":      "INS - Sprint 12",
    "sprint_id":        99999,
    "sprint_end_date":  datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    "ends_today":       True,
    "total_issues":     18,
    "completed_issues": 12,
    "bugs_fixed":       3,
    "story_points":     34,
    # ── new fields ───────────────────────────────────────
    "sprint_start_date": "2026-02-23T09:00:00.000Z",
    "user_stories":      6,
    "enhancements":      3,
    "fixes":             3,
}
# ─────────────────────────────────────────────────────────


# -----------------------------
# GET ALL BOARDS (PAGINATION)
# ── UNCHANGED ────────────────
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
# ── UNCHANGED ────────────────
# -----------------------------
def get_active_sprints(board_id):

    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint?state=active"
    response = requests.get(url, headers=headers, auth=auth)
    data = response.json()
    return data.get("values", [])


# ─────────────────────────────────────────────────────────
# GET CLOSED SPRINTS — NEW
# Only called in TEST_MODE to find recently ended sprints
# ─────────────────────────────────────────────────────────
def get_closed_sprints(board_id):

    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint?state=closed"
    response = requests.get(url, headers=headers, auth=auth)
    data = response.json()
    return data.get("values", [])


# -----------------------------
# GET SPRINT ISSUES
# ── UNCHANGED ────────────────
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
# ── UNCHANGED ────────────────
# -----------------------------
def sprint_ends_today(sprint):

    end_date_str = sprint.get("endDate")

    if not end_date_str:
        return False

    try:
        end_date_str_clean = end_date_str.replace("Z", "+00:00")
        end_dt = datetime.fromisoformat(end_date_str_clean)
        end_date_local = end_dt.astimezone().date()
        today = datetime.now().date()
        return end_date_local == today

    except Exception as e:
        print(f"  [WARN] Could not parse sprint endDate '{end_date_str}': {e}")
        return False


# ─────────────────────────────────────────────────────────
# CHECK IF SPRINT ENDED RECENTLY — NEW
# Used only in TEST_MODE
# ─────────────────────────────────────────────────────────
def sprint_ended_recently(sprint):

    end_date_str = sprint.get("endDate")

    if not end_date_str:
        return False

    try:
        end_date_str_clean = end_date_str.replace("Z", "+00:00")
        end_dt             = datetime.fromisoformat(end_date_str_clean)
        end_date_local     = end_dt.astimezone().date()
        today              = datetime.now().date()
        earliest           = today - timedelta(days=TEST_DAYS_BACK)
        return earliest <= end_date_local <= today

    except Exception as e:
        print(f"  [WARN] Could not parse sprint endDate '{end_date_str}': {e}")
        return False


# ─────────────────────────────────────────────────────────
# MAIN METRICS FUNCTION
# ── All original fields kept
# ── New fields added on top
# ─────────────────────────────────────────────────────────
def get_metrics():

    results = []
    boards  = get_all_boards()

    for board in boards:

        board_id   = board["id"]
        board_name = board["name"]

        print(f"\nChecking board: {board_name}")

        # In TEST_MODE: active + closed sprints
        # In production: only active (original behavior)
        sprints = get_active_sprints(board_id)
        if TEST_MODE:
            sprints = sprints + get_closed_sprints(board_id)

        if not sprints:
            print("  No active sprint")
            continue

        for sprint in sprints:

            sprint_id   = sprint["id"]
            sprint_name = sprint["name"]
            sprint_end  = sprint.get("endDate", "N/A")

            # In TEST_MODE: skip sprints that didn't end recently
            if TEST_MODE and not sprint_ended_recently(sprint):
                continue

            print(f"  Active sprint: {sprint_name} | Ends: {sprint_end}")

            issues = get_sprint_issues(sprint_id)

            total        = len(issues)
            done         = 0
            bugs         = 0
            story_points = 0
            user_stories = 0   # ← new
            enhancements = 0   # ← new
            fixes        = 0   # ← new

            for issue in issues:

                fields     = issue["fields"]
                status     = fields["status"]["name"].lower()
                issue_type = fields["issuetype"]["name"].lower()

                # ── Original fields ──────────────────────────────
                sp = fields.get("customfield_10016")
                if sp:
                    story_points += sp

                if "done" in status:
                    done += 1

                if issue_type == "bug":
                    bugs += 1

                # ── New fields ───────────────────────────────────
                if issue_type in ("story", "user story", "feature"):
                    user_stories += 1

                if issue_type in ("improvement", "change"):
                    enhancements += 1

                if issue_type == "bug":
                    fixes += 1

            results.append({
                # ── All original fields ──────────────────────────
                "project_name":     board_name,
                "sprint_name":      sprint_name,
                "sprint_id":        sprint_id,
                "sprint_end_date":  sprint_end,
                "ends_today":       sprint_ends_today(sprint),
                "total_issues":     total,
                "completed_issues": done,
                "bugs_fixed":       bugs,
                "story_points":     story_points,
                # ── New fields ───────────────────────────────────
                "sprint_start_date": sprint.get("startDate", "N/A"),
                "user_stories":      user_stories,
                "enhancements":      enhancements,
                "fixes":             fixes,
            })

            # Stop once we hit the MAX_SPRINTS limit
            if len(results) >= MAX_SPRINTS:
                print(f"\n  [LIMIT] Reached MAX_SPRINTS={MAX_SPRINTS}, stopping.")
                return results

    return results


# -----------------------------
# GET ONLY SPRINTS ENDING TODAY
# ── UNCHANGED ────────────────
# -----------------------------
def get_sprints_ending_today():

    all_metrics  = get_metrics()
    ending_today = [m for m in all_metrics if m.get("ends_today")]

    print(f"\nSprints ending today: {len(ending_today)}")

    # Real sprint found → use it, fake is ignored
    if ending_today:
        return ending_today

    # In TEST_MODE — return recently ended real sprints too
    if TEST_MODE and all_metrics:
        print(f"  [TEST] No sprint ending today — returning {len(all_metrics)} recent sprint(s)")
        return all_metrics

    # No real sprint today → fall back to fake if enabled
    if USE_FAKE_AS_FALLBACK:
        print("  No real sprint ending today — using FAKE sprint for testing")
        return [FAKE_SPRINT]

    return []


# -----------------------------
# RUN SCRIPT
# ── UNCHANGED ────────────────
# -----------------------------
if __name__ == "__main__":

    data = get_sprints_ending_today()

    print("\nFINAL RESULT:\n")
    print(data)