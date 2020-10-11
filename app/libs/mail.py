# @Time    : 2020/10/11 下午12:12

__author__ = 'xhb'


from flask_mail import Message
from app import mail
from flask import current_app, render_template


def send_mail(to, subject, template, **kwargs):
    msg = Message('[鱼书] ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)


