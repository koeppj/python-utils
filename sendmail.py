"""Send an email via smpt.

   For usage datails run "sendmail --help"
"""
import smtplib
import argparse
import time
from email.message import EmailMessage
from email.utils import formatdate


def prompt(prompt):
    return input(prompt).strip()

def prompt_miltiline(prompt):
    print(prompt)
    body = ''
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        if line.__len__ == 0:
            break
        body = body + line
    return body

def get_parser(): 
    """Builds the command line argument parser"""
    parser = argparse.ArgumentParser(
        description='Send an email via smtp',
        epilog="Can send via submission or via server after authentication")
    parser.add_argument('-s','--server',
                        type=str,
                        required=True,
                        help='The dommain or FQDN of the servr')
    parser.add_argument('-p','--port',
                        type=int,
                        required=False,
                        default=25,
                        help='The port.  Will default to as appropriate base on other args')
    parser.add_argument('--starttls',
                        action='store_const',
                        const=True,
                        help='If set try to use STARTTLS')
    parser.add_argument('-u','--username',
                        type=str,
                        required=False,
                        help='User name to use to authenticate, if no provided auth not tried')
    parser.add_argument('-t','--token',
                        type=str,
                        required=True,
                        help='Password to use to login (required if --username spacified)')
    return parser

def send_mail(args):

    # Build the Email object
    msg = EmailMessage()
    msg['To'] = prompt('To: ')
    msg['From'] = prompt('From: ')
    msg['Subject'] = prompt('Subject: ')
    msg['Date'] = formatdate()
    msg.set_content(prompt_miltiline("Enter message body (blank line when done)"))

    # Establish the connection to an email server and send the email.
    smtp = smtplib.SMTP(host=args.server,port=args.port)
    smtp.set_debuglevel(1)
    smtp.ehlo()
    if smtp.has_extn('STARTTLS'): 
        smtp.starttls()
        smtp.ehlo()
        if args.username:
            smtp.login(args.username,args.token)
    smtp.send_message(msg)
    smtp.quit()


if __name__ == "__main__":
    args = get_parser().parse_args()
    send_mail(args)