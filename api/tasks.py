from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import Currency
import itertools

@shared_task
# some heavy stuff here
def create_currency():
    req = Request('https://www.investing.com/currencies/single-currency-crosses',
                  headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urlopen(req).read()
    except (http.client.IncompleteRead) as e:
        html = e.partial
    soup = BeautifulSoup(html, 'html.parser')
    # get data for USD, EUR, JPY, GBP, AUD, CAD, CHF, CNH, SEK, NZD pair with INR
    
    table = soup.find("tbody").find_all("tr")
    index = [160, 1493, 1529, 1551, 1646, 1760, 1900, 2020, 1985]
    currency = []
    for tr in table:
        if(tr.attrs["id"]=="pair_160"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1493"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1529"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1551"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1646"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1760"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1900"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_2020"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1985"):
            currency.append(tr)

    for idx, cur in zip(index, currency):
        pair = cur.find("td", class_="plusIconTd").a.text
        bid = cur.find("td", class_=f"pid-{idx}-bid").text
        ask = cur.find("td", class_=f"pid-{idx}-ask").text
        high = cur.find("td", class_=f"pid-{idx}-high").text
        low = cur.find("td", class_=f"pid-{idx}-low").text
        change = cur.find("td", class_=f"pid-{idx}-pc").text
        change_p = cur.find("td", class_=f"pid-{idx}-pc").text
        time = cur.find("td", class_=f"pid-{idx}-time").text

        # create objects in database
        Currency.objects.create(
            pair=pair,
            bid=bid,
            ask=ask,
            high=high,
            low=low,
            change=change,
            change_p=change_p,
            time=time
        )

        # sleep few seconds to avoid database block
        sleep(5)


@shared_task
def update_currency():
    req = Request('https://www.investing.com/currencies/single-currency-crosses',
                  headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urlopen(req).read()
    except (http.client.IncompleteRead) as e:
        html = e.partial
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("tbody").find_all("tr")
    index = [160, 1493, 1529, 1551, 1646, 1760, 1900, 2020, 1985]
    currency = []
    for tr in table:
        if(tr.attrs["id"] == "pair_160"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1493"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1529"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1551"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1646"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1760"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1900"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_2020"):
            currency.append(tr)
        elif(tr.attrs["id"] == "pair_1985"):
            currency.append(tr)

    for idx, cur in zip(index, currency):
        pair = cur.find("td", class_="plusIconTd").a.text
        bid = cur.find("td", class_=f"pid-{idx}-bid").text
        ask = cur.find("td", class_=f"pid-{idx}-ask").text
        high = cur.find("td", class_=f"pid-{idx}-high").text
        low = cur.find("td", class_=f"pid-{idx}-low").text
        change = cur.find("td", class_=f"pid-{idx}-pc").text
        change_p = cur.find("td", class_=f"pid-{idx}-pc").text
        time = cur.find("td", class_=f"pid-{idx}-time").text
        # create dictionary
        data = {'pair': pair, 'bid': bid, 'ask': ask, 'high': high,
                'low': low, 'change': change, 'change_p': change_p, 'time': time}
        # find the object by filtering and update all fields
        Currency.objects.filter(pair=pair).update(**data)

        sleep(5)


create_currency()
while True:
    # updating data every 15 seconds
    sleep(20)
    update_currency()
