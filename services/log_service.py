import json
import psycopg2
from datetime import datetime
from config import DATABASE_URL


def get_connection():
    return psycopg2.connect(DATABASE_URL + "?sslmode=require")


def init_db():
    """
    Creates the email_logs table in PostgreSQL if it doesn't exist.

    Schema:
    ┌─────────────────┬──────────────────────────────────────────────────────┐
    │ id              │ Auto-increment primary key                           │
    │ sent_at         │ Timestamp when the email was sent (UTC)              │
    │ project_name    │ Jira board / project name                            │
    │ sprint_name     │ Sprint name                                          │
    │ sprint_id       │ Jira sprint ID                                       │
    │ sprint_end_date │ Sprint end date from Jira                            │
    │ client_email    │ Email address the NPS email was sent to              │
    │ status          │ 'sent' or 'failed'                                   │
    │ sprint_data     │ Full sprint metrics stored as JSONB                  │
    └─────────────────┴──────────────────────────────────────────────────────┘
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_logs (
            id              SERIAL PRIMARY KEY,
            sent_at         TIMESTAMP   NOT NULL DEFAULT NOW(),
            project_name    TEXT        NOT NULL,
            sprint_name     TEXT        NOT NULL,
            sprint_id       INTEGER     NOT NULL,
            sprint_end_date TEXT,
            client_email    TEXT        NOT NULL,
            status          TEXT        NOT NULL DEFAULT 'sent',
            sprint_data     JSONB
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def log_email(sprint, client_email, status="sent"):
    """
    Logs a sent (or failed) NPS email to PostgreSQL.

    Args:
        sprint       (dict)  : Full sprint dict from jira_service
        client_email (str)   : Recipient email address
        status       (str)   : 'sent' or 'failed'
    """
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO email_logs
            (sent_at, project_name, sprint_name, sprint_id,
             sprint_end_date, client_email, status, sprint_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        datetime.utcnow(),
        sprint.get("project_name"),
        sprint.get("sprint_name"),
        sprint.get("sprint_id"),
        sprint.get("sprint_end_date"),
        client_email,
        status,
        json.dumps(sprint)      # stored as JSONB — fully queryable in PgAdmin
    ))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"  [DB] Logged → {client_email} | {sprint.get('sprint_name')} | status={status}")


def already_sent_today(sprint_id):
    """
    Returns True if we already sent an email for this sprint_id today.
    Prevents duplicate emails if the action runs multiple times in a day.
    """
    init_db()

    today = datetime.utcnow().date()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM email_logs
        WHERE sprint_id = %s
          AND sent_at::date = %s
          AND status = 'sent'
    """, (sprint_id, today))

    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return count > 0


def get_all_logs():
    """Returns all rows from email_logs as a list of dicts."""
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, sent_at, project_name, sprint_name, sprint_id,
               sprint_end_date, client_email, status, sprint_data
        FROM email_logs
        ORDER BY sent_at DESC
    """)

    columns = [desc[0] for desc in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return rows