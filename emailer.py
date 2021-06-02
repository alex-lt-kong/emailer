#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime as dt
import json
import logging
import smtplib
import time


def send_service_start_notification(settings_path: str, service_name: str,
                                    log_path: str, tail=20, delay=300):

    time.sleep(delay)
    start_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(settings_path, 'r') as json_file:
            json_str = json_file.read()
            json_data = json.loads(json_str)
    except Exception as e:
        # What if logging is not configured?
        # Let's do it next time...
        logging.info(f'JSON error: {e}')
        return

    from_address = json_data['email']['from_address']
    from_password = json_data['email']['from_password']
    from_name = json_data['email']['from_name']
    to_address = json_data['email']['to_address']
    to_name = json_data['email']['to_name']

    lines = '[NA]'
    try:
        with open(log_path, 'r') as log_file:
            lines = log_file.readlines()[-1 * tail:]
            lines = '\n'.join(lines)
    except Exception as e:
        logging.info('Unable to read log file'
                     f'(notification will be sent anyway): {e}')

    mainbody = f'Service [{service_name}] started at {start_time}\n\n'
    mainbody += f'Latest log:\n{lines}'

    send(from_name=from_name,
         from_address=from_address, from_password=from_password,
         to_name=to_name, to_address=to_address,
         subject=f'Service [{service_name}] started',
         mainbody=mainbody,
         fontsize=2, log=True)


def send(from_name: str, from_address: str, from_password: str,
         to_name: str, to_address: str,
         subject: str, mainbody: str, fontsize=2, log=False):

    mainbody = mainbody.replace('\n', '<br>')
    msg = (
        f'From: {from_name} <{from_address}>\n'
        f'To: {to_name} <{to_address}>\n'
        'Content-Type: text/html; charset="UTF-8"\n'
        f'Subject: {subject}\n'
        '<meta http-equiv="Content-Type" content="text/html charset=UTF-8" />'
        f'<html><fontsize="{fontsize}" color="black">{mainbody}</font></html>')

    try:
        smtpObj = smtplib.SMTP(host='server172.web-hosting.com', port=587)
        smtpObj.starttls()
        smtpObj.login(from_address, from_password)
        smtpObj.sendmail(from_address, to_address, msg.encode('utf-8'))
        smtpObj.quit()
        if log:
            logging.debug(f'Email [{subject}] sent successfully')
    except Exception as e:
        logging.error(e)
