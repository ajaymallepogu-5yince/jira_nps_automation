from datetime import datetime

BOS_LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAPoAAAD6CAYAAACI7Fo9AAABCGlDQ1BJQ0MgUHJvZmlsZQAAeJxjYGA8wQAELAYMDLl5JUVB7k4KEZFRCuwPGBiBEAwSk4sLGHADoKpv1yBqL+viUYcLcKakFicD6Q9ArFIEtBxopAiQLZIOYWuA2EkQtg2IXV5SUAJkB4DYRSFBzkB2CpCtkY7ETkJiJxcUgdT3ANk2uTmlyQh3M/Ck5oUGA2kOIJZhKGYIYnBncAL5H6IkfxEDg8VXBgbmCQixpJkMDNtbGRgkbiHEVBYwMPC3MDBsO48QQ4RJQWJRIliIBYiZ0tIYGD4tZ2DgjWRgEL7AwMAVDQsIHG5TALvNnSEfCNMZchhSgSKeDHkMyQx6QJYRgwGDIYMZAKbWPz9HbOBQAAAC70lEQVR4nO3TwQ3AIBDAsKP77wxToErEniCfrJnZAzzt+zsAuM/oEGB0CDA6BBgdAowOAUaHAKNDgNEhwOgQYHQIMDoEGB0CjA4BRocAo0OA0SHA6BBgdAgwOgQYHQKMDgFGhwCjQ4DRIcDoEGB0CDA6BBgdAowOAUaHAKNDgNEhwOgQYHQIMDoEGB0CjA4BRocAo0OA0SHA6BBgdAgwOgQYHQKMDgFGhwCjQ4DRIcDoEGB0CDA6BBgdAowOAUaHAKNDgNEhwOgQYHQIMDoEGB0CjA4BRocAo0OA0SHA6BBgdAgwOgQYHQKMDgFGhwCjQ4DRIcDoEGB0CDA6BBgdAowOAUaHAKNDgNEhwOgQYHQIMDoEGB0CjA4BRocAo0OA0SHA6BBgdAgwOgQYHQKMDgFGhwCjQ4DRIcDoEGB0CDA6BBgdAowOAUaHAKNDgNEhwOgQYHQIMDoEGB0CjA4BRocAo0OA0SHA6BBgdAgwOgQYHQKMDgFGhwCjQ4DRIcDoEGB0CDA6BBgdAowOAUaHAKNDgNEhwOgQYHQIMDoEGB0CjA4BRocAo0OA0SHA6BBgdAgwOgQYHQKMDgFGhwCjQ4DRIcDoEGB0CDA6BBgdAowOAUaHAKNDgNEhwOgQYHQIMDoEGB0CjA4BRocAo0OA0SHA6BBgdAgwOgQYHQKMDgFGhwCjQ4DRIcDoEGB0CDA6BBgdAowOAUaHAKNDgNEhwOgQYHQIMDoEGB0CjA4BRocAo0OA0SHA6BBgdAgwOgQYHQKMDgFGhwCjQ4DRIcDoEGB0CDA6BBgdAowOAUaHAKNDgNEhwOgQYHQIMDoEGB0CjA4BRocAo0OA0SHA6BBgdAgwOgQYHQKMDgFGhwCjQ4DRIcDoEGB0CDA6BBgdAowOAUaHAKNDgNEh4ACX/ALzbcCD+QAAAABJRU5ErkJggg=="

NPS_FORM_URL = "https://docs.google.com/forms/d/1x-YbiK31FU5w_0rWmP4BtWnXX5cG-A8b3WKnYOT3Sgk/viewform"


def generate_summary(sprint):
    """
    Generates the HTML email body using the official BOS Framework
    NPS ail template with sprint details before the survey button.
    """

    project_name = sprint.get("project_name", "N/A")
    sprint_name  = sprint.get("sprint_name",  "N/A")
    end_date_raw = sprint.get("sprint_end_date", "N/A")
    total        = sprint.get("total_issues",     0)
    completed    = sprint.get("completed_issues", 0)
    bugs         = sprint.get("bugs_fixed",       0)
    points       = sprint.get("story_points",     0)
    completion   = round((completed / total) * 100) if total > 0 else 0

    # Format date → "March 09, 2026"
    try:
        dt       = datetime.fromisoformat(end_date_raw.replace("Z", "+00:00"))
        end_date = dt.strftime("%B %d, %Y")
    except Exception:
        end_date = end_date_raw

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Request for NPS Feedback – Quick Survey</title>
</head>
<body style="margin:0;padding:0;background:#efefef;font-family:'Georgia',serif;">

  <table width="100%" cellpadding="0" cellspacing="0"
         style="background:#efefef;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="620" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border:1px solid #d0d0d0;
                      border-radius:2px;">

          <!-- ══ HEADER — Logo + Brand ══ -->
          <tr>
            <td style="padding:28px 36px 22px;
                       border-bottom:2px solid #000000;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="vertical-align:middle;width:60px;">
                    <img src="data:image/png;base64,{BOS_LOGO_B64}"
                         alt="BOS Framework"
                         width="52"
                         style="display:block;" />
                  </td>
                  <td style="padding-left:14px;vertical-align:middle;">
                    <div style="font-size:19px;font-weight:bold;
                                color:#000000;letter-spacing:3px;">
                      BOS FRAMEWORK
                    </div>
                    <div style="font-size:10px;color:#888888;
                                letter-spacing:4px;text-transform:uppercase;
                                margin-top:3px;">
                      Sprint Completion Report
                    </div>
                  </td>
                  <td style="text-align:right;vertical-align:middle;">
                    <div style="font-size:11px;color:#aaaaaa;">
                      {end_date}
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- ══ SPRINT TITLE BAND ══ -->
          <tr>
            <td style="background:#000000;padding:16px 36px;">
              <div style="font-size:10px;color:#888888;letter-spacing:4px;
                          text-transform:uppercase;margin-bottom:4px;">
                Sprint Completed
              </div>
              <div style="font-size:19px;color:#ffffff;font-weight:bold;
                          letter-spacing:1px;">
                {sprint_name}
              </div>
              <div style="font-size:12px;color:#aaaaaa;margin-top:4px;">
                {project_name}
              </div>
            </td>
          </tr>

          <!-- ══ BODY ══ -->
          <tr>
            <td style="padding:32px 36px 8px;">

              <!-- GREETING + INTRO (from your template) -->
              <p style="margin:0 0 10px;font-size:15px;color:#222222;
                        line-height:1.85;">
                Dear Valued Client,
              </p>
              <p style="margin:0 0 10px;font-size:15px;color:#333333;
                        line-height:1.85;">
                I hope you are doing well.
              </p>
              <p style="margin:0 0 28px;font-size:15px;color:#333333;
                        line-height:1.85;">
                As part of our continuous improvement process, we would
                appreciate your feedback on the recent sprint. Your input
                helps us understand how satisfied you are with our delivery
                and how we can improve our services.
              </p>

              <!-- ── SPRINT DETAILS (before NPS button) ── -->
              <div style="font-size:10px;color:#888888;letter-spacing:4px;
                          text-transform:uppercase;margin-bottom:12px;">
                Sprint Summary
              </div>

              <table width="100%" cellpadding="0" cellspacing="0"
                     style="margin-bottom:32px;border:1px solid #e0e0e0;">

                <!-- Table header -->
                <tr style="background:#f5f5f5;">
                  <td style="padding:9px 16px;font-size:10px;color:#888888;
                              letter-spacing:3px;text-transform:uppercase;
                              border-bottom:1px solid #e0e0e0;">
                    Metric
                  </td>
                  <td style="padding:9px 16px;font-size:10px;color:#888888;
                              letter-spacing:3px;text-transform:uppercase;
                              text-align:right;
                              border-bottom:1px solid #e0e0e0;">
                    Value
                  </td>
                </tr>

                <!-- Sprint Name -->
                <tr>
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">
                    Sprint
                  </td>
                  <td style="padding:13px 16px;font-size:14px;font-weight:bold;
                              color:#000000;text-align:right;
                              border-bottom:1px solid #eeeeee;">
                    {sprint_name}
                  </td>
                </tr>

                <!-- End Date -->
                <tr style="background:#fafafa;">
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">
                    Completed On
                  </td>
                  <td style="padding:13px 16px;font-size:14px;font-weight:bold;
                              color:#000000;text-align:right;
                              border-bottom:1px solid #eeeeee;">
                    {end_date}
                  </td>
                </tr>

                <!-- Total Issues -->
                <tr>
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">
                    Total Issues
                  </td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:#000000;text-align:right;
                              border-bottom:1px solid #eeeeee;">
                    {total}
                  </td>
                </tr>

                <!-- Completed -->
                <tr style="background:#fafafa;">
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">
                    Completed
                  </td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:#000000;text-align:right;
                              border-bottom:1px solid #eeeeee;">
                    {completed}
                    <span style="font-size:12px;color:#999999;
                                 font-weight:normal;">
                      &nbsp;({completion}%)
                    </span>
                  </td>
                </tr>

                <!-- Bugs Fixed -->
                <tr>
                  <td style="padding:13px 16px;font-size:14px;color:#444444;
                              border-bottom:1px solid #eeeeee;">
                    Bugs Fixed
                  </td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:#000000;text-align:right;
                              border-bottom:1px solid #eeeeee;">
                    {bugs}
                  </td>
                </tr>

                <!-- Story Points -->
                <tr style="background:#fafafa;">
                  <td style="padding:13px 16px;font-size:14px;color:#444444;">
                    Story Points Delivered
                  </td>
                  <td style="padding:13px 16px;font-size:17px;font-weight:bold;
                              color:#000000;text-align:right;">
                    {points}
                  </td>
                </tr>

              </table>

              <!-- ── NPS SURVEY SECTION ── -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="margin-bottom:32px;border:1px solid #000000;">
                <tr>
                  <td style="padding:24px 24px 28px;">

                    <div style="font-size:10px;color:#888888;letter-spacing:4px;
                                text-transform:uppercase;margin-bottom:12px;">
                      Share Your Feedback
                    </div>

                    <p style="margin:0 0 8px;font-size:15px;color:#222222;
                               line-height:1.8;">
                      Please take a moment to complete our short NPS survey
                      using the link below.
                    </p>
                    <p style="margin:0 0 22px;font-size:15px;color:#333333;
                               line-height:1.8;">
                      The survey will only take a minute, and your feedback
                      is highly valuable to our team.
                    </p>

                    <a href="{NPS_FORM_URL}"
                       style="display:inline-block;background:#000000;
                              color:#ffffff;text-decoration:none;
                              padding:14px 32px;font-size:11px;
                              letter-spacing:3px;text-transform:uppercase;">
                      Take the Survey &rarr;
                    </a>

                  </td>
                </tr>
              </table>

              <!-- SIGN OFF (from your template) -->
              <p style="margin:0 0 6px;font-size:15px;color:#333333;
                        line-height:1.85;">
                Thank you for your time and continued collaboration.
              </p>
              <p style="margin:0 0 6px;font-size:15px;color:#333333;">
                Best regards,
              </p>
              <p style="margin:0 0 32px;font-size:15px;color:#000000;
                        font-weight:bold;">
                BOS Framework Team
              </p>

              <!-- Disclaimer -->
              <p style="margin:0 0 28px;font-size:11px;color:#aaaaaa;
                        line-height:1.7;">
                This is an automated notification from the BOS Framework
                delivery team. Please do not reply to this email directly.
              </p>

            </td>
          </tr>

          <!-- ══ FOOTER ══ -->
          <tr>
            <td style="background:#000000;padding:16px 36px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="color:#666666;font-size:11px;letter-spacing:1px;">
                    &copy; BOS Framework &nbsp;&middot;&nbsp; bosframework.com
                  </td>
                  <td style="text-align:right;color:#555555;font-size:11px;">
                    {end_date}
                  </td>
                </tr>
              </table>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>"""

    return html