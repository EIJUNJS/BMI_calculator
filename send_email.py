import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(email, BMI):
    from_email = "shao19980209@gmail.com"
    password = "qynmhrwryuouetzi"
    mail_to = email

    mail_subject = "This is your BMI report"
    mail_body = """
        <h3>Hi，all</h3>
        <p>Your BMI value is <strong>%s</strong>.</p>
        """ % BMI
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = mail_to
    msg['Subject'] = mail_subject
    msg.attach(MIMEText(mail_body, _subtype='html'))
    connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
    connection.starttls()
    connection.login(from_email, password)
    connection.send_message(msg)
    connection.quit()
