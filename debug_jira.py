"""
Run this in PyCharm with SPRINT_ID = 4659
to see exact status + issue type names from Jira
"""

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

JIRA_EMAIL     = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL  = os.getenv("JIRA_BASE_URL")

auth    = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = { "Accept": "application/json" }

SPRINT_ID = 4659   # ← INS - Sprint 12

url      = f"{JIRA_BASE_URL}/rest/agile/1.0/sprint/{SPRINT_ID}/issue?maxResults=100"
response = requests.get(url, headers=headers, auth=auth)
issues   = response.json().get("issues", [])

print(f"\nTotal Issues: {len(issues)}")
print("\n" + "-"*75)
print(f"{'KEY':<12} {'STATUS':<30} {'TYPE':<25} {'SUMMARY'}")
print("-"*75)

statuses = {}
types    = {}

for issue in issues:
    fields     = issue["fields"]
    key        = issue["key"]
    status     = fields["status"]["name"]
    issue_type = fields["issuetype"]["name"]
    summary    = fields.get("summary", "")[:30]

    print(f"{key:<12} {status:<30} {issue_type:<25} {summary}")

    statuses[status]  = statuses.get(status, 0) + 1
    types[issue_type] = types.get(issue_type, 0) + 1

print("\n" + "="*50)
print("UNIQUE STATUSES")
print("="*50)
for s, c in sorted(statuses.items()):
    print(f"  '{s}' → {c} issue(s)")

print("\n" + "="*50)
print("UNIQUE ISSUE TYPES")
print("="*50)
for t, c in sorted(types.items()):
    print(f"  '{t}' → {c} issue(s)")