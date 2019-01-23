import requests
from bs4 import BeautifulSoup as bs
import arrow
import csv
import pandas as pd

def sfwm():
    month = input("Please enter the number of the month in the form '1':  ")
    for l in range(1, 13):
        if month == str(l):
            mnum = month
            mnum = mnum.zfill(2)
            break
        elif (l == 12) & (str(month) != l):
            print("Please enter a valid option")
            sfwm()

    year = input("Please enter a year in the form '18'")
    for yr in range(18, 100):
        if year == str(yr):
            year_name = arrow.get(year, 'YY').format('YYYY')
            break
        elif (yr == 99) & (str(yr) != year):
            print("Please enter a valid input")
            sfwm()

    site_url = "https://www.sfwmpac.org/calendar-of-events/"+year_name+"-"+mnum+"-10"
    plain_url = site_url.replace("/calendar-of-events/"+year_name+"-"+mnum+"-10", "")
    venue = "San Francisco War Memorial"
    price = 'NaN'

    site = requests.get(site_url)
    soup = bs(site.content, 'lxml')
    urls = [x.get('href') for x in soup.find_all('a', class_="event-info")]
    site_urls = [plain_url + url for url in urls]

    events = []
    times = []
    dates = []
    for url in site_urls:
        site = requests.get(url)
        soup = bs(site.content, 'lxml')

        if "Herbst" in (soup.find(class_="detail-block")).text:
            full_date = (soup.find(class_="full-date")).text
            split_date = full_date.split(",")
            year = split_date[-1]
            mday = split_date[1]
            raw_date = mday + year
            date = arrow.get(raw_date, " MMMM D YYYY").format("MM/DD/YY")
            dates.append(date)

            time = (soup.find(class_="time")).text
            time = time.replace('\n', '')
            times.append(time)

            event = (soup.find('h4')).text
            event = event.replace('\n', '')
            event = event.lstrip()
            event = event.rstrip()
            events.append(event)
        else:
            continue

    # t = ""
    # # tries to read csv, if not creates or empty them headers are added
    # try:
    #     df = pd.read_csv('sfwm.csv')
    # except FileNotFoundError:
    #     t = "NaN"
    # except pd.errors.EmptyDataError:
    #     t = 'NaN'
    # if t == 'NaN':
    with open('sfwm.csv', 'w') as ttable:
        filewriter = csv.writer(ttable)
        filewriter.writerow(["Venue", "Event", "Date", "Time", "Price"])
    # Appends all of the elements in our lists to the csv
    with open('sfwm.csv', 'a', encoding='utf-8') as ttable:
        filewriter = csv.writer(ttable)
        for b in range(0, len(events)):
            filewriter.writerow([venue, events[b], dates[b], times[b], price])

    x = True
    while x:
        redo = input("Would you like to choose anothe rmonth? [y/n]")
        if redo.upper() == "N":
            print("Goodbye")
            x = False
        elif redo.upper() == "Y":
            sfwm()
            x = False
        else:
            print("Please enter a valid input")
            x = True

sfwm()