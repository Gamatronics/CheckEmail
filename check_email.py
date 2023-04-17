import imaplib
import email
import os
import email_credentials as emailcreds

# connect to the email account
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(emailcreds.emailAdress, emailcreds.password)
mail.select('inbox')

# search for emails from a specific sender
sender = 'example@example.com'
typ, data = mail.search(None, f'(FROM "{sender}")')

# loop through the emails and extract information
for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    
    # extract the subject and body
    subject = msg['Subject']
    body = msg.get_payload(decode=True).decode()
    
    # perform the action if the subject contains a keyword
    if 'keyword' in subject:
        # save the attachment to disk
        for part in msg.walk():
            if part.get_content_type() == 'application/pdf':
                filename = part.get_filename()
                if filename:
                    with open(filename, 'wb') as f:
                        f.write(part.get_payload(decode=True))
        # send a reply email
        mail.sendmail('your_email_address', sender, 'Thanks for your email!')
    
mail.close()
mail.logout()
