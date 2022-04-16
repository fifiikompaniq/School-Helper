import smtplib
import time
import imaplib
import email
import traceback 

ORG_EMAIL   = "@elsys-bg.org"
FROM_EMAIL  = "yosif.g.saltiel.2020" + ORG_EMAIL
FROM_PWD    = "MyNameIsJeff"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993



def read_mail(): 
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_date = msg['дата']
                    email_from = msg['от']
                    print('From : ' + email_from + '\n')
                    print('Date : ' + email_date + '\n')

    except Exception as e:
        traceback.print_exc() 
        print(str(e))

    

def main():
    read_mail()




if __name__ == '__main__': 
    main()