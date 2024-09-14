current_site = 'emilys-luxury.com'
# rest_password_url = 'https://emily-sa.vercel.app/auth/reset-password'
rest_password_url = 'https://emily.sa/auth/reset-password'

def create_otp_template(user_name , OTP , user_email):
    otp_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8" />
    <title></title>
    <style>
        body {{
        margin: 0;
        padding: 0;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        color: #333;
        background-color: #fff;
        }}

        .container {{
        margin: 0 auto;
        width: 100%;
        max-width: 600px;
        padding: 0 0px;
        padding-bottom: 10px;
        border-radius: 5px;
        line-height: 1.8;
        }}
        .header {{
        border-bottom: 1px solid #eee;
        }}
        .header a {{
        font-size: 1.4em;
        color: #000;
        text-decoration: none;
        font-weight: 600;
        }}

        .content {{
        min-width: 700px;
        overflow: auto;
        line-height: 2;
        }}

        .otp {{
        background: linear-gradient(to right, #00bc69 0, #00bc88 50%, #00bca8 100%);
        margin: 0 auto;
        width: max-content;
        padding: 0 10px;
        color: #fff;
        border-radius: 4px;
        }}

        .footer {{
        color: #aaa;
        font-size: 0.8em;
        line-height: 1;
        font-weight: 300;
        }}

        .email-info {{
        color: #666666;
        font-weight: 400;
        font-size: 13px;
        line-height: 18px;
        padding-bottom: 6px;
        }}

        .email-info a {{
        text-decoration: none;
        color: #00bc69;
        }}
    </style>
    </head>

    <body>
    <!--Subject: Login Verification Required for Your Emily Account-->
    <div class="container">
        <div class="header">
        <a>Emily.sa</a>
        </div>
        <br />
        <strong>Dear {user_name},</strong>
        <p>
        We have received a login request for your Emily.sa account. For
        security purposes, please verify your identity by providing the
        following One-Time Password (OTP).
        <br />
        <b>Your One-Time Password (OTP) verification code is:</b>
        </p>
        <h2 class="otp">{OTP}</h2>
        <p style="font-size: 0.9em">
        <strong>One-Time Password (OTP) is valid for 15 minutes.</strong>
        <br />
        <br />
        If you did not initiate this login request, please disregard this
        message. Please ensure the confidentiality of your OTP and do not share
        it with anyone.<br />
        <strong>Do not forward or give this code to anyone.</strong>
        <br />
        <br />
        <strong>Thank you for using Emily.sa.</strong>
        <br />
        <br />
        Best regards,
        <br />
        <strong>Emily.sa</strong>
        </p>

        <hr style="border: none; border-top: 0.5px solid #131111" />
        <div class="footer">
        <p>This email can't receive replies.</p>
        <p>
            For more information about Emily and your account, visit
            <strong>Emily.sa</strong>
        </p>
        </div>
    </div>
    <div style="text-align: center">
        <div class="email-info">
        <span>
            This email was sent to
            <a href="mailto:{user_email}">{user_email}</a>
        </span>
        </div>
        <div class="email-info">
        <a href="/">Emily.sa</a> | Saudi Arabia
        </div>
        <div class="email-info">
        &copy; 2024 Emily.sa  All rights
        reserved.
        </div>
    </div>
    </body>
    </html>
    """
    return otp_template
