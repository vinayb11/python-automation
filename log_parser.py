#!/usr/bin/env python2.7
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import sys

match_list = []
lines = ""
count = 0
count_old = 0
#print count
#print count_old
###print (count == count_old)
with open("/var/log/syslog", "r") as f:
    for line in f:
        if "Error message to be searched in logs" in line:
            count = count + 1
            match_list.append(line)
            lines = '\n'.join(match_list)
if count == 0:
    print "No Error found"
    sys.exit(0)
with open("/tmp/count_old_errors", "r") as f1:
    count_old = (int(f1.read()))

if count == count_old:
    sys.exit(0)
else:
    count_old = count
    with open("/tmp/count_old_errors", "w") as fp:
        fp.write(str(count))
        fp.close
    s = smtplib.SMTP('localhost')
    body = lines
    msg = MIMEText(body)
    sender = 'root@localhost.com'
    recipients = ['vinayb11@hotmail.com']
    msg['Subject'] = "Error trap"
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    s.sendmail(sender, recipients, msg.as_string())
    print "CRITICAL: Email Sent"
    sys.exit(2)
