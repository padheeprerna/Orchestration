# CONFIDENTIAL COMPUTER CODE AND INFORMATION
# COPYRIGHT (C) VMware, INC. ALL RIGHTS RESERVED.
# REPRODUCTION BY ANY MEANS EXPRESSLY FORBIDDEN WITHOUT THE WRITTEN
# PERMISSION OF THE OWNER.
# 
#  A UTILITY TO SEND EMAIL USING VMWARE SMTP
#####################################################################


# Import standard modules
import os, sys, optparse, smtplib, socket
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEMessage import MIMEMessage
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


def send_email(from_, to, subject, body, cc=[], attachments=[],
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
        assert type(to)==list

        # CC Recipients
        assert type(cc)==list
        
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
            part.set_payload( open(file,"rb").read() )
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'
                            % os.path.basename(file))
            msg.attach(part)
            
        # Process email
        smtp = smtplib.SMTP(smtp_server)
        smtp.sendmail(from_, to+cc, msg.as_string())		
        smtp.close()
        
        # Exceptional scenarios
    except socket.gaierror as err:
        return False, "HTTP connection failure"
    except socket.error as err:
        return False, "HTTP connection error"
    except smtplib.SMTPException as err:
        return False, "Error:  %s"%(err)
    except smtplib.SMTPServerDisconnected as err:
        return False, "Error:  %s"%(err)
    except smtplib.SMTPResponseException as err:
        return False, "Error:  %s"%(err)
    except smtplib.SMTPSenderRefused as err:
        return False, "Error:  %s"%(err)
    except smtplib.SMTPDataError as err:
        return False, "Error:  %s"%(err)
    except smtplib.SMTPConnectError as err:
        return False, "Error:  %s"%(err)
    except smtplib.SMTPHeloError as err:
        return False, "Error:  %s"%(err)
    except smtplib.SMTPAuthenticationError as err:
        return False, "Error:  %s"%(err)
    else:
        return True, "Mail sent successfully..."            



if __name__ == '__main__':
    # ------------------------------------------------------------------------
    # SUPPORTED COMMANDLINE ARGUMENTS
    # ------------------------------------------------------------------------
    parser = optparse.OptionParser()
    parser.add_option('-f', '--from', dest="_from",
                          help="From", default="")
    parser.add_option('-t', '--to', dest="to",
                          help="To: Recipients with comma seperated delimiters", default="")
    parser.add_option('-c', '--cc', dest="cc",
                          help="Cc: Recipients with comma seperated delimiters|Optional", default="")
    parser.add_option('-s', '--sub', dest="sub",
                          help="Subject line", default="")
    parser.add_option('-b', '--body', dest="body",
                          help="Message Body", default="")
    parser.add_option('-a', '--attach', dest="attach",
                          help="Attachments: Absolute path of files with comma seperated delimiters|Optional", default="")
    options, args = parser.parse_args()


    # Launch help on invalid commandline options...
    if len(sys.argv) == 1: # No options
        parser.print_help()
        sys.exit(1)

    # -------------------------------------------------------------------------
    # READ ARGUMENTS
    # -------------------------------------------------------------------------     
    _from  = options._from
    to = options.to.split(',')
    if options.cc:
        cc = options.cc.split(',')
    else:
	cc = []
    sub = options.sub
    body = options.body
    if options.attach:
        attach = options.attach.split(',')
    else:
	attach = []
     
    # -------------------------------------------------------------------------
    # SEND EMAIL NOTIFICATION
    # -------------------------------------------------------------------------     
    send_email(_from, to, sub, body, cc, attachments=attach)

       
