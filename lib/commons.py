# CONFIDENTIAL COMPUTER CODE AND INFORMATION
# COPYRIGHT (C) VMware, INC. ALL RIGHTS RESERVED.
# REPRODUCTION BY ANY MEANS EXPRESSLY FORBIDDEN WITHOUT THE WRITTEN
# PERMISSION OF THE OWNER.
#
# COMMONLY USED METHODS
# ----------------------------------------------------------------------------

# STANDARD LIBRARIES
import os, sys
import time, datetime
import traceback

import bencode as bencode
from jinja2 import Template
import hashlib
import json

# USER DEFINED LIBRARIES 
from settings import APPS
from settings import MAIL_CONFIG, NOTIFICATION
from mail import send_email


def sleep(seconds):
    """
	Wait till given time is elapsed
    """
    time.sleep(seconds)


def get_app_name(app_type):
    """
	Returns application name
    """
    return APPS[app_type]['name']


def get_job_name(app_type):
    """
	Returns jenkins job name
    """
    return APPS[app_type]['job']


def get_defects_header(app_type):
    """
	Returns defects header for report
    """
    return APPS[app_type]['header']


def get_localtime():
    """
        Returns present date and time
    """
    localtime = time.strftime("%A %B %d %Y %I:%M:%S %p %Z", time.localtime())
    return localtime


def get_timestamp():
    """
	Returns present timestamp
    """
    return int(time.time())


def get_timenow():
    """
        Returns current time
    """
    # return (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return datetime.datetime.now()


def get_datenow():
    """
	Returns current date
    """
    return datetime.datetime.now().strftime('%d-%m-%Y')


def get_report_path(report_base, app_type):
    """
        Returns report path
    """
    date_now = get_datenow()
    timestamp = get_timestamp()
    report_path = os.path.join(report_base, app_type, str(date_now), str(timestamp))
    debug_path = os.path.join(report_path, 'debug')
    if not os.path.exists(report_path):
        os.makedirs(report_path, mode = 0o777)
        os.makedirs(debug_path, mode = 0o777)
    return report_path


def get_report_name(report_path, report_ext):
    """
        Returns report name
    """
    return os.path.join(report_path, 'report.' + report_ext)


def get_log_name(report_path):
    """
	Returns log name
    """
    return os.path.join(report_path, 'debug.log')


def get_logfile(LOGS):
    """
	Returns current log file name
    """
    curr_date = get_datenow()
    log_name = 'debug_' + str(get_timestamp()) + '.log'
    logs_dir = os.path.join(LOGS, curr_date)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    log_file = os.path.join(logs_dir, log_name)
    return log_file


def get_debugger(LOGS):
    """
	Returns current log file name
	LOGS should be a report_path: output from get_report_path()
    """

    log_name = 'debug.log'
    logs_dir = LOGS
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    log_file = os.path.join(logs_dir, log_name)
    return log_file


def get_pst_time(timestamp):
    """
        Returns PST time for the given timestamp
    """
    fmt = "%A %B %d %Y %I:%M:%S %p %Z"
    # Timezone [PST]: America/Los_Angeles
    pst_timezone = time.timezone('America/Los_Angeles')
    now_time = datetime.datetime.fromtimestamp(timestamp, tz=pst_timezone)
    return now_time.strftime(fmt)


def get_ist_time(timestamp):
    """
        Returns IST time for the given timestamp
    """
    fmt = "%A %B %d %Y %I:%M:%S %p %Z"
    # Timezone [IST]: Asia/Calcutta
    ist_timezone = time.timezone('Asia/Calcutta')
    now_time = datetime.datetime.fromtimestamp(timestamp, tz=ist_timezone)
    return now_time.strftime(fmt)


def is_perforce_path(json):
    """
	Returns True if input filepath is from perforce, False otherwise
    """
    # Todo: Future enhancement
    return False


def encrypt(txt):
    """
	Returns encrypted string
    """
    return txt.encode('base64', 'strict')


def decrypt(txt):
    """
	Returns decrypted string
    """
    return txt.decode('base64', 'strict')


def get_dict_checksum(dict):
    """
	Returns checksum of dictionary
    """
    return hashlib.md5(bencode.bencode(dict)).hexdigest()


def capture_traceback(log):
    """
        Capture error tracebacks on exceptional scenarios
        Call this method in all except blocks
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    formatted_lines = traceback.format_exc().splitlines()
    log.record('debug', '>' * 100)
    for line in formatted_lines:
        log.record('debug', line)
    log.record('debug', '>' * 100)


def send_notification(app_name, rfc, project_name, exec_id, rows):
    """
        Sends an email notification on overall execution status
    """
    _from = MAIL_CONFIG['FROM']
    to = MAIL_CONFIG['TO']
    cc = MAIL_CONFIG['CC']
    sub = MAIL_CONFIG['SUB'] + ' ' + app_name
    header = MAIL_CONFIG['HEADER']

    template = Template(NOTIFICATION)
    _dict_ = {'app_name': app_name, 'rfc': rfc, 'project_name': project_name,
              'vrcs_exec_id': exec_id, 'header': header, 'rows': rows
              }
    body = template.render(_dict_)

    status, msg = send_email(_from, to, sub, body, cc)
    return status
