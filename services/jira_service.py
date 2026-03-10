import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from config import JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json"
}

# ─────────────────────────────────────────────────────────────────────────────
# CONTROLS
#
#   TEST_MODE = True
#   ├── Looks AHEAD by TEST_DAYS_AHEAD days to find sprints ending soon
#   ├── Also includes active sprints ending today
#   ├── USE_FAKE_AS_FALLBACK = True → falls back to fake sprint if nothing found
#   └── Useful for: previewing upcoming sprint emails before they fire
#
#   TEST_MODE = False  ← PRODUCTION
#   ├── Only processes sprints ending EXACTLY today
#   ├── No look-back, no look-ahead, no fake data
#   └── USE_FAKE_AS_FALLBACK is ignored entirely
#
#   MAX_SPRINTS → cap how many sprints are processed per run
#
# ── TO GO LIVE ────────────────────────────────────────────────────────────────
#   TEST_MODE            = False
#   USE_FAKE_AS_FALLBACK = False   (already ignored, but good to be explicit)
# ─────────────────────────────────────────────────────────────────────────────

TEST_MODE            = True
TEST_DAYS_AHEAD      = 5        # look this many days forward in TEST_MODE
MAX_SPRINTS          = 2
USE_FAKE_AS_FALLBACK = True

FAKE_SPRINT = {
    "project_name":      "INVStudio-StrongPosition",
    "sprint_name":       "INS - Sprint 12",
    "sprint_id":         99999,
    "sprint_end_date":   datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    "ends_today":        True,
    "total_issues":      18,
    "completed_issues":  12,
    "bugs_fixed":        3,
    "story_points":      34,
    "sprint_start_date": "2026-02-23T09:00:00.000Z",
    "user_stories":      6,
    "enhancements":      3,
    "fixes":             3,
    "tasks":             3,
}
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — parse a Jira endDate string → local date
# ─────────────────────────────────────────────────────────────────────────────
def _parse_end_date(sprint):
    end_date_str = sprint.get("endDate")
    if not end_date_str:
        return None
    try:
        end_dt = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
        return end_dt.astimezone().date()
    except Exception as e:
        print(f"  [WARN] Could not parse sprint endDate '{end_date_str}': {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# CHECK IF SPRINT ENDS TODAY  (used in both modes)
# ─────────────────────────────────────────────────────────────────────────────
def sprint_ends_today(sprint):
    end_date_local = _parse_end_date(sprint)
    if end_date_local is None:
        return False
    return end_date_local == datetime.now().date()


# ─────────────────────────────────────────────────────────────────────────────
# CHECK IF SPRINT ENDS WITHIN THE NEXT N DAYS  (TEST_MODE only)
# Includes today so today's sprints are never missed
# ─────────────────────────────────────────────────────────────────────────────
def sprint_ends_within_days_ahead(sprint):
    end_date_local = _parse_end_date(sprint)
    if end_date_local is None:
        return False
    today   = datetime.now().date()
    cutoff  = today + timedelta(days=TEST_DAYS_AHEAD)
    return today <= end_date_local <= cutoff


# ─────────────────────────────────────────────────────────────────────────────
# GET ALL BOARDS  (pagination)
# ─────────────────────────────────────────────────────────────────────────────
def get_all_boards():
    boards     = []
    start_at   = 0
    max_results = 50

    while True:
        url      = f"{JIRA_BASE_URL}/rest/agile/1.0/board?startAt={start_at}&maxResults={max_results}"
        response = requests.get(url, headers=headers, auth=auth)
        data     = response.json()
        values   = data.get("values", [])
        boards.extend(values)

        if data.get("isLast", True):
            break

        start_at += max_results

    print(f"\nTotal boards found: {len(boards)}")
    return boards


# ─────────────────────────────────────────────────────────────────────────────
# GET ACTIVE SPRINTS for a board
# ─────────────────────────────────────────────────────────────────────────────
def get_active_sprints(board_id):
    url      = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint?state=active"
    response = requests.get(url, headers=headers, auth=auth)
    return response.json().get("values", [])


# ─────────────────────────────────────────────────────────────────────────────
# GET SPRINT ISSUES  (pagination)
# ─────────────────────────────────────────────────────────────────────────────
def get_sprint_issues(sprint_id):
    issues     = []
    start_at   = 0
    max_results = 50

    while True:
        url      = f"{JIRA_BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue?startAt={start_at}&maxResults={max_results}"
        response = requests.get(url, headers=headers, auth=auth)
        data     = response.json()
        batch    = data.get("issues", [])
        issues.extend(batch)

        if start_at + max_results >= data.get("total", 0):
            break

        start_at += max_results

    return issues


# ─────────────────────────────────────────────────────────────────────────────
# MAIN METRICS FUNCTION
#
#   PRODUCTION (TEST_MODE = False):
#     → Only fetches ACTIVE sprints
#     → Only includes sprints ending exactly today
#
#   TEST MODE (TEST_MODE = True):
#     → Fetches ACTIVE sprints
#     → Includes sprints ending today OR within the next TEST_DAYS_AHEAD days
#     → Does NOT look back at closed/past sprints
# ─────────────────────────────────────────────────────────────────────────────
def get_metrics():
    results = []
    boards  = get_all_boards()

    for board in boards:
        board_id   = board["id"]
        board_name = board["name"]
        location   = board.get("location", {})

        print(f"\nChecking board: {board_name} → space: {location.get('projectName') or board_name}")

        # Always only look at ACTIVE sprints — no closed sprint lookback
        sprints = get_active_sprints(board_id)

        if not sprints:
            print("  No active sprint")
            continue

        for sprint in sprints:
            sprint_id   = sprint["id"]
            sprint_name = sprint["name"]
            sprint_end  = sprint.get("endDate", "N/A")

            # ── PRODUCTION: must end today ────────────────────────────────────
            if not TEST_MODE and not sprint_ends_today(sprint):
                print(f"  [SKIP] {sprint_name} | Ends: {sprint_end} — not today")
                continue

            # ── TEST MODE: must end today OR within next TEST_DAYS_AHEAD days ─
            if TEST_MODE and not sprint_ends_within_days_ahead(sprint):
                print(f"  [SKIP] {sprint_name} | Ends: {sprint_end} — outside {TEST_DAYS_AHEAD}-day window")
                continue

            print(f"  {'[TEST] ' if TEST_MODE else ''}Sprint: {sprint_name} | Ends: {sprint_end}")

            issues       = get_sprint_issues(sprint_id)
            done         = 0
            story_points = 0
            user_stories = 0   # Jira type: Story, User Story
            enhancements = 0   # Jira type: Improvement, Change
            fixes        = 0   # Jira type: Bug
            tasks        = 0   # Jira type: Task

            # Subtasks are always excluded from all counts
            SUBTASK_TYPES = {"subtask", "sub-task", "subtasks", "sub task"}

            # Statuses that count as completed in your Jira
            COMPLETED_STATUSES = {
                "done", "closed", "resolved",
                "ready for production", "pass", "complete", "completed"
            }

            for issue in issues:
                fields     = issue["fields"]
                status     = fields["status"]["name"].lower()
                issue_type = fields["issuetype"]["name"].lower()

                # ── Skip subtasks entirely ───────────────────────────────────
                if issue_type in SUBTASK_TYPES:
                    continue

                sp = fields.get("customfield_10016")
                if sp:
                    story_points += sp

                # ── Bucket by type (only 4 recognised types count) ───────────
                if issue_type in ("story", "user story"):
                    user_stories += 1
                elif issue_type in ("improvement", "change"):
                    enhancements += 1
                elif issue_type == "bug":
                    fixes += 1
                elif issue_type == "task":
                    tasks += 1
                else:
                    continue  # not a counted type — also excluded from completed

                # Completed ONLY counted for the 4 bucket types above
                # This ensures completed <= total always
                if status in COMPLETED_STATUSES:
                    done += 1



            # Total always = sum of 4 buckets — guaranteed to match
            total = user_stories + enhancements + fixes + tasks

            # Sanity check — completed can never exceed total
            if done > total:
                print(f"  [WARN] completed({done}) > total({total}) — capping at total")
                done = total
            print(f"  → Total: {total} | Completed: {done} | Stories: {user_stories} | Enhancements: {enhancements} | Fixes: {fixes} | Tasks: {tasks}")
            bugs  = fixes   # bugs_fixed = fixes (both = Bug type)

            # Space name = projectName (clean, no key suffix like "(STF)")
            # Falls back to board name if location not available
            space_name = (
                location.get("projectName")
                or board_name
            )

            results.append({
                "project_name":      space_name,
                "sprint_name":       sprint_name,
                "sprint_id":         sprint_id,
                "sprint_end_date":   sprint_end,
                "ends_today":        sprint_ends_today(sprint),
                "total_issues":      total,
                "completed_issues":  done,
                "bugs_fixed":        bugs,
                "story_points":      story_points,
                "sprint_start_date": sprint.get("startDate", "N/A"),
                "user_stories":      user_stories,
                "enhancements":      enhancements,
                "fixes":             fixes,
                "tasks":             tasks,
            })

            if len(results) >= MAX_SPRINTS:
                print(f"\n  [LIMIT] Reached MAX_SPRINTS={MAX_SPRINTS}, stopping.")
                return results

    return results


# ─────────────────────────────────────────────────────────────────────────────
# GET SPRINTS TO PROCESS
#
#   PRODUCTION (TEST_MODE = False):
#     → Returns only sprints ending today
#     → Returns [] if none found — NO fake fallback
#
#   TEST MODE (TEST_MODE = True):
#     → Returns sprints ending today OR within next TEST_DAYS_AHEAD days
#     → Falls back to FAKE_SPRINT only if USE_FAKE_AS_FALLBACK = True
#       and no real sprints were found at all
# ─────────────────────────────────────────────────────────────────────────────
def get_sprints_ending_today():
    all_metrics  = get_metrics()
    ending_today = [m for m in all_metrics if m.get("ends_today")]

    print(f"\nSprints ending today: {len(ending_today)}")

    # Sprints ending exactly today — always return these first
    if ending_today:
        return ending_today

    # TEST MODE only: also include sprints ending within next N days
    if TEST_MODE and all_metrics:
        print(f"  [TEST] No sprint ending today — returning {len(all_metrics)} sprint(s) ending within {TEST_DAYS_AHEAD} days")
        return all_metrics

    # TEST MODE only: fake fallback if nothing found at all
    if TEST_MODE and USE_FAKE_AS_FALLBACK:
        print("  [TEST] No real sprint found — using FAKE sprint for testing")
        return [FAKE_SPRINT]

    # PRODUCTION: nothing ending today → do nothing
    print("  No sprint ending today — nothing to send")
    return []


# ─────────────────────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    data = get_sprints_ending_today()
    print("\nFINAL RESULT:\n")
    print(data)