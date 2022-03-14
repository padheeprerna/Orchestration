# CONFIDENTIAL COMPUTER CODE AND INFORMATION
# COPYRIGHT (C) VMware, INC. ALL RIGHTS RESERVED.
# REPRODUCTION BY ANY MEANS EXPRESSLY FORBIDDEN WITHOUT THE WRITTEN
# PERMISSION OF THE OWNER.
# 
#  A UTILITY TO SEND EMAIL USING VMWARE SMTP
__author__ = "shivarajs"

#####################################################################


# Import standard modules
import os, smtplib, socket
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.message import MIMEMessage
from email.mime.text import MIMEText
from email.utils import formatdate  # COMMASPACE,
from email import encoders

COMMASPACE = ', '


def send_email(from_, to, subject, body, attachments=[], cc=[],
               smtp_server='smtp.vmware.com'):
    """
        Method to send email using vmware SMTP
        Arguments:
        from_   = string
        to      = List of recipients with comma seperated delimiter
        subject = Email subject
        body    = Mail message content
        attachments = List of absolute path of files
    """
    try:
        # Recipients
        assert type(to) == list

        # CC Recipients
        assert type(cc) == list

        # MIME Part with message details
        msg = MIMEMultipart()
        # Record the MIME types as text/html.
        part = MIMEText(body, 'html')

        # Email headers
        msg['From'] = from_
        msg['To'] = COMMASPACE.join(to)
        msg['Cc'] = COMMASPACE.join(cc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        # Attach parts into message container.
        # According to RFC 2046: part of a multipart message,
        # In this case HTML message, is best and preferred.
        msg.attach(part)

        # Attachments
        for file in attachments:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'
                            % os.path.basename(file))
            msg.attach(part)

        # Process email
        smtp = smtplib.SMTP(smtp_server)
        smtp.sendmail(from_, to + cc, msg.as_string())
        smtp.close()

        # Exceptional scenarios
    except socket.gaierror as err:
        return False, "HTTP connection failure"
    except socket.error as err:
        print("here")
        return False, "HTTP connection error"
    except smtplib.SMTPException as err:
        return False, "Error:  %s" % (err)
    except smtplib.SMTPServerDisconnected as err:
        return False, "Error:  %s" % (err)
    except smtplib.SMTPResponseException as err:
        return False, "Error:  %s" % (err)
    except smtplib.SMTPSenderRefused as err:
        return False, "Error:  %s" % (err)
    except smtplib.SMTPDataError as err:
        return False, "Error:  %s" % (err)
    except smtplib.SMTPConnectError as err:
        return False, "Error:  %s" % (err)
    except smtplib.SMTPHeloError as err:
        return False, "Error:  %s" % (err)
    except smtplib.SMTPAuthenticationError as err:
        return False, "Error:  %s" % (err)
    else:
        return True, "Mail sent successfully..."

    # Invoke send_mail
# from_ = "anandkishor@vmware.com"
# to = ["pankaja@vmware.com"]  # coma seperated email list
# subject = "Test Notification"
# body = "Email body here..."
# attachments=[] # ABsolute path of file
# cc = ["pankaja@vmware.com"] # coma seperated email list
# send_email(from_, to, subject, body, attachments, cc)
