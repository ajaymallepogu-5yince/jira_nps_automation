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