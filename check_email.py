from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        #results = service.users().labels().list(userId='me').execute()
        #labels = results.get('labels', [])
        results = service.users().messages().list(userId='me',labelIds=['INBOX'], q='is:unread').execute()
        messagesList = results.get('messages',[])
        counter = 0 #check 10 emails
        for msg in messagesList:
            messagesGet = service.users().messages().get(userId='me', id=msg['id']).execute()
            counter+=1
        #print(messagesList[0])
        #print(messagesGet['payload']['headers'])
        #print(messagesGet['payload']['headers'][22]['value'])
        #quit()
            
            for x in range(len(messagesGet['payload']['headers'])):
                
                #print(messagesGet['payload']['headers'][x]['name'])
                if messagesGet['payload']['headers'][x]['name'] == 'Subject':
                    subject = messagesGet['payload']['headers'][x]['value']
                    if subject == 'Gast, see your April updates.':
                        print('Found the right email')
                        quit()
                    print('Subject:',subject)
            if counter > 10: 
                print("no hay nada en los primeros diez", counter)
                break



    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
'''
        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])
'''



if __name__ == '__main__':
    main()