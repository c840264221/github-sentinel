import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown2


class EmailSender:
    def __init__(self, smtp_server, port, sender_email, auth_code):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.auth_code = auth_code

    def send_email(self, to_email, subject, content):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        html_body = markdown2.markdown(
            content,
            extras=["fenced-code-blocks", "tables"]
        )
        html_template = f"""
        <html>
        <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
        }}

        h1, h2, h3 {{
            color: #2c3e50;
        }}

        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 4px;
        }}

        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            overflow-x: auto;
            border-radius: 6px;
        }}

        table {{
            border-collapse: collapse;
        }}

        table, th, td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}

        </style>
        </head>
        <body>
        {html_body}
        </body>
        </html>
        """

        msg.attach(MIMEText(html_template, "html", "utf-8"))

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
                server.login(self.sender_email, self.auth_code)
                server.sendmail(self.sender_email, to_email, msg.as_string())
            print(f"✅ Email sent to {to_email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")


if __name__ == '__main__':
    sender = EmailSender(
        smtp_server="smtp.qq.com",
        port=465,
        sender_email="448851139@qq.com",
        auth_code="ieervxwdifelbgcc"
    )

    sender.send_email(
        to_email="745135150@qq.com",
        subject="测试",
        content="测试内容"
    )