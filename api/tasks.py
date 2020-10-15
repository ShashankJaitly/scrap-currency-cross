from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import Currency


@shared_task
# some heavy stuff here
def create_currency():
    req = Request('https://www.investing.com/currencies/single-currency-crosses',
                  headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    # get data for USD, EUR, JPY, GBP, AUD, CAD, CHF, CNH, SEK, NZD pair with INR
    index = [160, 1493, 1529, 1551, 1646, 1760, 1900, 2020, 1985]

    usd = soup.find("tbody").find("tr", id_="pair_160")
    aud = soup.find("tbody").find("tr", id_="pair_1493")
    cad = soup.find("tbody").find("tr", id_="pair_1529")
    chf = soup.find("tbody").find("tr", id_="pair_1551")
    eur = soup.find("tbody").find("tr", id_="pair_1646")
    gbp = soup.find("tbody").find("tr", id_="pair_1760")
    jpy = soup.find("tbody").find("tr", id_="pair_1900")
    sek = soup.find("tbody").find("tr", id_="pair_2020")
    nzd = soup.find("tbody").find("tr", id_="pair_1985")

    
    currencies = [usd, aud, cad, chf, eur, gbp, jpy, sek, nzd]

    for idx, currency in index , currencies:
        pair = currency.find("td", class_="plusIconTd").a.text
        bid = currency.find("td", class_=f"pid-{idx}-bid").text
        ask = currency.find("td", class_=f"pid-{idx}-ask").text
        high = currency.find("td", class_=f"pid-{idx}-high").text
        low = currency.find("td", class_=f"pid-{idx}-low").text
        change = currency.find("td", class_=f"pid-{idx}-pc").text
        change_p = currency.find("td", class_=f"pid-{idx}-pc").text
        time = currency.find("td", class_=f"pid-{idx}-time").text

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
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    index = [160, 1493, 1529, 1551, 1646, 1760, 1900, 2020, 1985]

    usd = soup.find("tbody").find("tr", id_="pair_160")
    aud = soup.find("tbody").find("tr", id_="pair_1493")
    cad = soup.find("tbody").find("tr", id_="pair_1529")
    chf = soup.find("tbody").find("tr", id_="pair_1551")
    eur = soup.find("tbody").find("tr", id_="pair_1646")
    gbp = soup.find("tbody").find("tr", id_="pair_1760")
    jpy = soup.find("tbody").find("tr", id_="pair_1900")
    sek = soup.find("tbody").find("tr", id_="pair_2020")
    nzd = soup.find("tbody").find("tr", id_="pair_1985")

    currencies = [usd, aud, cad, chf, eur, gbp, jpy, sek, nzd]
    for idx, currency in index, currencies:
        pair = currency.find("td", class_="plusIconTd").a.text
        bid = currency.find("td", class_=f"pid-{idx}-bid").text
        ask = currency.find("td", class_=f"pid-{idx}-ask").text
        high = currency.find("td", class_=f"pid-{idx}-high").text
        low = currency.find("td", class_=f"pid-{idx}-low").text
        change = currency.find("td", class_=f"pid-{idx}-pc").text
        change_p = currency.find("td", class_=f"pid-{idx}-pc").text
        time = currency.find("td", class_=f"pid-{idx}-time").text

        # create dictionary
        data = {'pair': pair, 'bid': bid, 'ask': ask, 'high': high,
                'low': low, 'change': change, 'change_p': change_p, 'time': time}
        # find the object by filtering and update all fields
        Currency.objects.filter(pair=pair).update(**data)

        sleep(5)


create_currency()
while True:
    # updating data every 15 seconds
    sleep(10)
    update_currency()
