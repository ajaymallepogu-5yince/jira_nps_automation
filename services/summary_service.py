from datetime import datetime

BOS_LOGO_B64 = "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"

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
                    <img src="data:image/jpeg;base64,{BOS_LOGO_B64}" alt="BOS" width="130" style="display:block;" />
                  </td>
                  <td style="padding-left:20px;vertical-align:middle;border-left:2px solid #e0e0e0;">
                    <div style="font-size:18px;font-weight:bold;
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
                Dear Valued Client,
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
                  <td style="padding:13px 16px;font-size:14px;color:#444444;">Fixes</td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:{BRAND_COLOR};text-align:right;">{fixes}</td>
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
                BOS Framework Team
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