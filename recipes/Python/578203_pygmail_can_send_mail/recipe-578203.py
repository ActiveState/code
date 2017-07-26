# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 20:57:29 2012

@author: garrett
@email: cloudform511@gmail.com
original pygmail from:
    https://github.com/vinod85/pygmail/blob/master/pygmail.py
    
"""

import imaplib, smtplib
import re

from email.mime.text import MIMEText

class pygmail(object):
    IMAP_SERVER='imap.gmail.com'
    IMAP_PORT=993
    
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT=465
        
    def __init__(self):
        self.M = None
        self.response = None
        self.mailboxes = []

    def login(self, username, password):
        self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        self.S = smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT)
        rc, self.response = self.M.login(username, password)
        sc, self.response_s = self.S.login(username, password)
        self.username = username
        return rc, sc

    def send_mail(self, to_addrs, msg, subject = None):
        msg = MIMEText(msg)
        if subject != None:
            msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_addrs
        return self.S.sendmail(self.username, to_addrs, msg.as_string())
        
    def get_mailboxes(self):
        rc, self.response = self.M.list()
        for item in self.response:
            self.mailboxes.append(item.split()[-1])
        return rc

    def get_mail_count(self, folder='Inbox'):
        rc, self.response = self.M.select(folder)
        return self.response[0]

    def get_unread_count(self, folder='Inbox'):
        rc, self.response = self.M.status(folder, "(UNSEEN)")
        unreadCount = re.search("UNSEEN (\d+)", self.response[0]).group(1)
        return unreadCount

    def get_imap_quota(self):
        quotaStr = self.M.getquotaroot("Inbox")[1][1][0]
        r = re.compile('\d+').findall(quotaStr)
        if r == []:
            r.append(0)
            r.append(0)
        return float(r[1])/1024, float(r[0])/1024

    def get_mails_from(self, uid, folder='Inbox'):
        status, count = self.M.select(folder, readonly=1)
        status, response = self.M.search(None, 'FROM', uid)
        email_ids = [e_id for e_id in response[0].split()]
        return email_ids

    def get_mail_from_id(self, id):
        status, response = self.M.fetch(id, '(body[header.fields (subject)])')
        return response

    def rename_mailbox(self, oldmailbox, newmailbox):
        rc, self.response = self.M.rename(oldmailbox, newmailbox)
        return rc

    def create_mailbox(self, mailbox):
        rc, self.response = self.M.create(mailbox)
        return rc

    def delete_mailbox(self, mailbox):
        rc, self.response = self.M.delete(mailbox)
        return rc

    def logout(self):
        self.M.logout()
        self.S.quit()

if __name__ == '__main__':
    user = 'vegans@gmail.com'
    pwd = 'govegan4life'
    gm = pygmail()
    gm.login(user, pwd)
    
    send_to = 'meat_eating_friend@gmail.com'
    msg = 'Hi there, have you ever thought about the suffering of animals? Go vegan!'
    gm.send_mail(send_to, msg, 'peace')
