import smtplib
import time
import datetime
import requests
import csv
import shutil

c_hour = '07'
c_minute = '56'


def send_email(recip, body):

    gmail_user = 'woodcockj@britishschoolmuscat.com'
    gmail_password = 'B2Spirit'

    sent_from = gmail_user

    to = [recip]
    subject = 'Subject: ARK Innovation'
    body = body

    email_text = f'{subject} \n\n {body}'

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        print('Email Setup Complete')

        server.sendmail(sent_from, to, email_text)
        print('Email sent')

        server.close()

        print('Server Closed')

    except:
        print('Rip something went wrong in the sending of the email')


def website_stuff():
    url = 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv'

    req = requests.get(url)

    url_content = req.content

    csv_file = open('newfile.csv', 'wb')
    csv_file.write(url_content)
    csv_file.close()


def compare_files():
    # compares files and generates the email body

    newfile = open('newfile.csv', 'r')

    new_reader = csv.DictReader(newfile)

    oldfile = open('oldfile.csv', 'r')
    old_reader = csv.DictReader(oldfile)

    # [ticker, num_shares, market_value]
    # [ticker, changed_shared]

    add_tickers = []
    changed_tickers = []
    delted_tickers = []

    new_tickers = []
    old_tickers = []

    print('Comparing')

    # add

    for old_row in old_reader:
        old_tickers.append(old_row['ticker'])

    for row in new_reader:
        new_tickers.append(row['ticker'])

    newfile.seek(0)

    for row in new_reader:

        if row['ticker'] != 'ticker' and row['ticker'] not in old_tickers:

            print('{} is not there'.format(row['ticker']))
            add_tickers.append(
                [row['ticker'], row['shares'], row['market value($)']])

    newfile.seek(0)
    oldfile.seek(0)

    for row in new_reader:

        for old_row in old_reader:

            if old_row['ticker'] == row['ticker'] and old_row['ticker'] != '':

                if old_row['shares'] != row['shares']:
                    print(old_row['shares'])
                    old_shares = float(old_row['shares'])
                    new_shares = float(row['shares'])

                    ticker = row['ticker']
                    change_shares = new_shares - old_shares

                    changed_tickers.append([ticker, change_shares])
        oldfile.seek(0)

    newfile.seek(0)
    oldfile.seek(0)

    for old_row in old_reader:
        if old_row['ticker'] != 'ticker' and old_row['ticker'] not in new_tickers:
            delted_tickers.append([old_row['ticker']])

    #shutil.copy('newfile.csv', 'oldfile.csv')

    return add_tickers, changed_tickers, delted_tickers


if __name__ == '__main__':

    website_stuff()

    print('Completed website stuff')

    add, changed, deleted = compare_files()

    m_added = 'TICKER/SHARES/MARKETVALUE b '

    for x in add:
        m_added += '\n'
        m_added += f'{x[0]}/{x[1]}/{x[2]}'

    m_changed = 'TICKER/SHARES'

    for x in changed:
        m_changed += '\n'
        m_changed += f'{x[0]}/{x[1]}'

    m_sold = 'TICKER'

    for x in deleted:
        m_sold += '\n'
        m_sold += f'{x[0]}'

    message = f'Welcome dad for etf update of the day \n\nNew stocks\n\n{m_added}\n\nChanged stocks\n\n{m_changed}\n\nFully sold stocks\n\n{m_sold}'
    print('\n\n\n')
    print(message)

    #send_email('adywoodcock@yahoo.co.uk', body=message)

    '''
    while True:
        
        current_time = str(datetime.datetime.now())

        hour = current_time[11:13]
        minute = current_time[14:16]

        print(hour, minute)

        if hour == c_hour and minute == c_minute:
            
            print('It is {}:{}'.format(c_hour, c_minute))
            
            website_stuff()
            
        
        else:      
            print('It is not {}:{}'.format(c_hour, c_minute))
            
        time.sleep(10)
        '''
