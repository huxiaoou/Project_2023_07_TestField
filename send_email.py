import os
import sys
import datetime as dt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header


def get_attachment(exe_date: str, orders_and_positions_dir: str):
    msg_file = f"huxo_{exe_date}.csv"
    msg_path = os.path.join(orders_and_positions_dir, exe_date[0:4], exe_date, msg_file)
    attachment_txt = MIMEApplication(open(msg_path, "rb").read())
    attachment_txt.add_header("Content-Disposition", "attachment", filename=msg_file)
    return attachment_txt


def get_body_message(exe_date: str):
    body_msg = f"{exe_date}日"
    return body_msg


if __name__ == "__main__":
    exe_date = sys.argv[1]

    # receivers
    receivers = [
        "<lhtz@ghzq.com.cn>",
        "<huxo@ghzq.com.cn>",
    ]

    # senders information
    mail_host = "mail.ghzq.com.cn"  # "113.16.174.142"
    mail_port = 25  # 465
    mail_sender = "huxo@ghzq.com.cn"
    mail_pwd = "Pkusms@100871"
    orders_and_positions_dir = r"E:\Deploy\Data\Futures\trades3\orders_and_positions"

    # message
    message = MIMEMultipart()
    message["From"] = "<{}>".format(mail_sender)
    message["To"] = ",".join(receivers)
    message["Subject"] = Header(f"huxo-CTA-Orders-{exe_date}", "utf-8")
    message.attach(MIMEText(get_body_message(exe_date)))
    message.attach(get_attachment(exe_date, orders_and_positions_dir))

    # send
    try:
        # smtp_app = smtplib.SMTP_SSL(mail_host, mail_port)
        smtp_app = smtplib.SMTP(mail_host, mail_port)
        print("... connected @ {}".format(dt.datetime.now()))
        smtp_app.login(mail_sender, mail_pwd)
        print("... logged in @ {}".format(dt.datetime.now()))
        smtp_app.sendmail(mail_sender, receivers, message.as_string())
        print("... 邮件发送成功 @ {}\n".format(dt.datetime.now()))
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件")
        print(e)
        print("\n")
