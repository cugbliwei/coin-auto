from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 

def send_mail(subject, content):
    try:
        from_address = '1192120201@qq.com'
        passwd = 'calsyieaqqyeibdf'
        to_address = [from_address]
         
        msg = MIMEMultipart()
        msg.attach(MIMEText(content,'plain','utf-8'))
        msg['Subject'] = subject
        msg['From'] = from_address
         
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(from_address, passwd)
        s.sendmail(from_address, to_address, msg.as_string())
    except:
        print('发送邮件失败')
