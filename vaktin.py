import time
import datetime
import smtplib
import requests
import pandas as pd
from bs4 import BeautifulSoup

def send_email( tee_time, freeslots):
    sender = 'golfvaktin@golfvaktinmin.is'
    receivers = ['birgir.palsson@gmail.com']

    message =  'Available tee time at ' + str(tee_time) + ' for ' + str(freeslots)+ ' persones.'
 

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com:587')
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login('birgir.itunes@gmail.com', 'Genesis.1966')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")

def empty_slots( tees ):
    s = 0
    for index, row in tees.iterrows():
        if not row["name"]:
            s = s + 1

    return s

def find_slot():
    dags = '2018-07-01'
    gr = 100
    grafarholt = 49
    korpa = 50
    start_time = 1000
    end_time = 1340
    players = 1
    found_slots = False

    url = "http://mitt.golf.is/pages/rastimar/rastimayfirlit/?hvenaer=0&hvar=" + str(
        grafarholt) + "&search=1&club=100&day=" + dags
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html5lib")
    tbody = soup.find_all("tbody")
    len(tbody)
    tbody = tbody[0]  # since find_all above returns a list

    table_rows = tbody.find_all("tr")

    len(table_rows)

    table_list = []

    current_time = None
    new_time = 0
    for tr in table_rows:
        rowspan_td = tr.find("td", {"rowspan": True})
        if rowspan_td:
            # if tr contains a td element with the rowspan attribute
            current_time = rowspan_td.text.strip()
            if ':' in current_time:
                new_time = int(current_time.replace(':', ''))
            else:
                new_time = -1
        int(new_time)
        table_list.append(
            [
                new_time,
                tr.find("td", {"class": "name"}).text.strip(),
                tr.find("td", {"class": "club"}).text.strip(),
                tr.find("td", {"class": "handicap"}).text.strip(),
                tr.find("td", {"class": "number-of-holes"}).text.strip(),
                tr.find("td", {"class": "unregister-from-round"}).text.strip()
            ])
    cols = ["time", "name", "club", "handicap", "num_holes", "unregistered"]
    df = pd.DataFrame(table_list, columns=cols)

    df.query('time>=@start_time and time<=@end_time', True)
    times = df.time.unique()

    # Loop over the tee times in the time range
    for ttime in times:
        tee_time = df.query('time==@ttime')
        e = empty_slots(tee_time)
        #print(str(ttime) + ': ' + str(e))
        if e >= players:
            send_email(ttime, e)
            found_slots = True
            break

    return found_slots

def main():
    print("Starting...")
    while not find_slot():
        now = datetime.datetime.now()
        print(now.strftime("%H:%M"))

        time.sleep(60)
    print("Done - email sent...")

if __name__== "__main__":
  main()


