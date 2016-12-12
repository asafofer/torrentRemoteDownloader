#! python 3
# torrentRemoteDownloader.py - a program that reads a specific mail account
# and downloads torrent via sent torrent magnet link

import imapclient, smtplib, sys, pyzmail,webbrowser,subprocess,time

password = sys.argv[1]
my_mail = 'XXXX@gmail.com' # Enter your mail
bot_mail = 'XXXX@gmail.com' # Enter your bot mail

# log in to the bot account to read command
imapObj = imapclient.IMAPClient('imap.gmail.com',ssl=True)
imapObj.login(bot_mail, password)
print('Logged in.')
imapObj.select_folder('INBOX')
UIDs = imapObj.search(['FROM ' + my_mail])

# log in to the bot account to send message
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(bot_mail, password)

while True:
    for UID in UIDs:
        rawMessages = imapObj.fetch([UID],['BODY[]'])
        message = pyzmail.PyzMessage.factory(rawMessages[UID][b'BODY[]'])
        subject = message.get_subject()
        if subject == 'Yo bot!': # Can change to a different command
            print('Getting instructions from mail')
            command = message.text_part.get_payload().decode(message.text_part.charset)
            if command.startswith('magnet:?'):
                subprocess.Popen(PATH_TO_TORRENT.EXE+' '+ command)
                imapObj.delete_messages(UID) # delete command mail to prevent it from preforming it again
                smtpObj.sendmail(bot_mail,my_mail,'Subject:Torrent status\nStarted downloading')
                print('Done Processing. Sleeping for 15 minutes')
                time.sleep(15*60)
