from datetime import datetime

BOS_LOGO_B64 = "https://www.bosframework.com/images/LogoBOS.png"

NPS_FORM_URL = "https://docs.google.com/forms/d/1x-YbiK31FU5w_0rWmP4BtWnXX5cG-A8b3WKnYOT3Sgk/viewform"
BRAND_COLOR  = "#00224C"


def _fmt_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y")
    except Exception:
        return date_str


def generate_summary(sprint):

    project_name = sprint.get("project_name",     "N/A")
    sprint_name  = sprint.get("sprint_name",       "N/A")
    start_raw    = sprint.get("sprint_start_date", "N/A")
    end_raw      = sprint.get("sprint_end_date",   "N/A")
    total        = sprint.get("total_issues",       0)
    completed    = sprint.get("completed_issues",   0)
    user_stories = sprint.get("user_stories",       0)
    enhancements = sprint.get("enhancements",       0)
    fixes        = sprint.get("fixes",              0)
    tasks        = sprint.get("tasks",              0)
    completion   = round((completed / total) * 100) if total > 0 else 0

    start_date = _fmt_date(start_raw)
    end_date   = _fmt_date(end_raw)
    year       = datetime.utcnow().strftime("%Y")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BOS: Sprint completed. Request for NPS Feedback - Quick Survey</title>
</head>
<body style="margin:0;padding:0;background:#efefef;font-family:'Georgia',serif;">

  <table width="100%" cellpadding="0" cellspacing="0"
         style="background:#efefef;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="620" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border:1px solid #d0d0d0;border-radius:2px;">

          <!-- HEADER — logo bigger, side by side with project name -->
          <tr>
            <td style="padding:24px 36px 20px;border-bottom:2px solid {BRAND_COLOR};">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="vertical-align:middle;width:140px;">
                    <img src="https://www.bosframework.com/images/LogoBOS.png" alt="BOS" width="130" style="display:block;" />
                  </td>
                  <td style="padding-left:20px;vertical-align:middle;border-left:2px solid #e0e0e0;">
                    <div style="font-size:28px;font-weight:bold;
                                color:{BRAND_COLOR};letter-spacing:1px;line-height:1.3;">
                      {project_name}
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- SPRINT TITLE BAND — sprint name only -->
          <tr>
            <td style="background:{BRAND_COLOR};padding:16px 36px;">
              <div style="font-size:10px;color:#a0b4cc;letter-spacing:4px;
                          text-transform:uppercase;margin-bottom:6px;">
                Sprint Completed
              </div>
              <div style="font-size:19px;color:#ffffff;font-weight:bold;
                          letter-spacing:1px;">
                {sprint_name}
              </div>
            </td>
          </tr>

          <!-- BODY -->
          <tr>
            <td style="padding:32px 36px 8px;">

              <p style="margin:0 0 10px;font-size:15px;color:#222222;line-height:1.85;">
                Dear Team {project_name},
              </p>
              <p style="margin:0 0 10px;font-size:15px;color:#333333;line-height:1.85;">
                I hope you are doing well.
              </p>
              <p style="margin:0 0 28px;font-size:15px;color:#333333;line-height:1.85;">
                As part of our continuous improvement process, we would
                appreciate your feedback on the recent sprint. Your input
                helps us understand how satisfied you are with our delivery
                and how we can improve our services.
              </p>

              <!-- SPRINT SUMMARY TABLE -->
              <div style="font-size:10px;color:#888888;letter-spacing:4px;
                          text-transform:uppercase;margin-bottom:12px;">
                Sprint Summary
              </div>

              <table width="100%" cellpadding="0" cellspacing="0"
                     style="margin-bottom:32px;border:1px solid #e0e0e0;">

                <tr>
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;width:55%;">Sprint</td>
                  <td style="padding:13px 16px;font-size:14px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;
                              border-bottom:1px solid #eeeeee;">{sprint_name}</td>
                </tr>

                <tr style="background:#fafafa;">
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">Start Date</td>
                  <td style="padding:13px 16px;font-size:14px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;
                              border-bottom:1px solid #eeeeee;">{start_date}</td>
                </tr>

                <tr>
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">End Date</td>
                  <td style="padding:13px 16px;font-size:14px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;
                              border-bottom:1px solid #eeeeee;">{end_date}</td>
                </tr>

                <tr style="background:#fafafa;">
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">Total Work Items</td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;
                              border-bottom:1px solid #eeeeee;">{total}</td>
                </tr>

                <tr>
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">Completed Items</td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;
                              border-bottom:1px solid #eeeeee;">
                    {completed}
                    <span style="font-size:12px;color:#999999;
                                 font-weight:normal;">&nbsp;({completion}%)</span>
                  </td>
                </tr>

                <tr style="background:#fafafa;">
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">User Stories</td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;
                              border-bottom:1px solid #eeeeee;">{user_stories}</td>
                </tr>

                <tr>
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">Enhancements</td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;
                              border-bottom:1px solid #eeeeee;">{enhancements}</td>
                </tr>

                <tr style="background:#fafafa;">
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">Fixes</td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;
                              border-bottom:1px solid #eeeeee;">{fixes}</td>
                </tr>

                <tr>
                  <td style="padding:13px 16px;font-size:14px;color:#444444;">Tasks</td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;">{tasks}</td>
                </tr>

              </table>

              <!-- NPS SURVEY -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="margin-bottom:32px;border:1px solid {BRAND_COLOR};">
                <tr>
                  <td style="padding:24px 24px 28px;">
                    <div style="font-size:10px;color:#888888;letter-spacing:4px;
                                text-transform:uppercase;margin-bottom:12px;">
                      Share Your Feedback
                    </div>
                    <p style="margin:0 0 8px;font-size:15px;color:#222222;line-height:1.8;">
                      Please take a moment to complete our short NPS survey
                      using the link below.
                    </p>
                    <p style="margin:0 0 22px;font-size:15px;color:#333333;line-height:1.8;">
                      The survey will only take a minute, and your feedback
                      is highly valuable to our team.
                    </p>
                    <a href="{NPS_FORM_URL}"
                       style="display:inline-block;background:{BRAND_COLOR};
                              color:#ffffff;text-decoration:none;
                              padding:14px 32px;font-size:11px;
                              letter-spacing:3px;text-transform:uppercase;">
                      Take the Survey &rarr;
                    </a>








                  </td>
                </tr>
              </table>

              <p style="margin:0 0 6px;font-size:15px;color:#333333;line-height:1.85;">
                Thank you for your time and continued collaboration.
              </p>
              <p style="margin:0 0 6px;font-size:15px;color:#333333;">Best regards,</p>
              <p style="margin:0 0 32px;font-size:15px;color:{BRAND_COLOR};font-weight:bold;">
                BOS Team
              </p>
              <p style="margin:0 0 28px;font-size:11px;color:#aaaaaa;line-height:1.7;">
                This is an automated notification from the BOS Framework
                delivery team. Please do not reply to this email directly.
              </p>

            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background:{BRAND_COLOR};padding:20px 36px;">
              <p style="margin:0 0 6px;color:#ffffff;font-size:12px;
                        font-weight:bold;letter-spacing:1px;">
                &copy; {year} &nbsp; BOS Framework
              </p>
              <p style="margin:0;">
                <a href="https://bosframework.com"
                   style="color:#a0b4cc;font-size:11px;
                          text-decoration:underline;letter-spacing:1px;">
                  BOSFramework.com
                </a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>"""

    return html