def generate_summary(sprint):
    """
    Generates a plain-text email body from the sprint metrics dict
    returned by jira_service.get_sprints_ending_today().

    Expected keys in sprint:
        project_name, sprint_name, sprint_id,
        sprint_end_date, ends_today,
        total_issues, completed_issues, bugs_fixed, story_points
    """

    project_name = sprint.get("project_name", "N/A")
    sprint_name  = sprint.get("sprint_name",  "N/A")
    end_date     = sprint.get("sprint_end_date", "N/A")
    total        = sprint.get("total_issues",    0)
    completed    = sprint.get("completed_issues", 0)
    bugs         = sprint.get("bugs_fixed",       0)
    points       = sprint.get("story_points",     0)

    completion_rate = round((completed / total) * 100) if total > 0 else 0

    summary = f"""Hi,

Your sprint has been completed for project: {project_name}

Sprint Details:
  Sprint Name     : {sprint_name}
  End Date        : {end_date}

Sprint Metrics:
  Total Issues    : {total}
  Completed       : {completed} ({completion_rate}%)
  Bugs Fixed      : {bugs}
  Story Points    : {points}

We would love to hear your feedback on this sprint.
Please take a moment to fill out our short NPS survey — it only takes 60 seconds!

Thank you for your continued collaboration.

Best regards,
The Delivery Team
"""

    return summary