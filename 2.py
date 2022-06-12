import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import time
from aiogram.utils import executor
from aiogram import Bot, Dispatcher

TOKEN = '5122624917:AAEnUBnJai7EJYOj8iBpP9tOKugi5n8jHQE'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def somefunc():
    await bot.send_message(1080509959, "Запуск")

if __name__ == '__main__':
    executor.start(dp, somefunc())



url = "https://www.earningswhispers.com/calendar"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",

}

def status(old, new, ed):
    if old > new:
        percent = (old/new*100)-100
        bt = '🔴'
        if percent > 30:
            bt = '🔴🔴'
        if percent > 60:
            bt = '🔴🔴🔴'
        if percent > 100:
            bt = '🔴🔴🔴🔴'

        stat = f'{bt} {ed} уменьшился на {percent:.1f}% {bt}'
    
    elif new > old:
        percent = (new/old*100)-100
        bt = '🟢'
        if percent > 30:
            bt = '🟢🟢'
        if percent > 60:
            bt = '🟢🟢🟢'
        if percent > 100:
            bt = '🟢🟢🟢🟢'
        

        stat = f'{bt} {ed} увеличился на {percent:.1f}% {bt}'
    
    elif new == old:
        stat = f'🔘{ed} не изменился🔘'
    
    return stat
        
def numbers(number):
    b = ''
    j = 1
    k = ''
    if number[0] == '(':
        k = '-'
    if number[-1] == 'B':
        s = 'M'
        j = 1000

    elif number[-1] == 'M':
        s = 'M'
    else:
        s = ''
    for i in number:
        if i.isnumeric() or i == '.':
            b += i
    b = float(b) * j
    b = k + str(b)
    return float(b), s

def start(url, finded):
    src = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(src.text, "html.parser")
    try:
        eps = soup.find('ul', id = finded)
        li = eps.find_all('li')
    except:
        pass
    try:
        for ticker in li:
            try:
                name = ticker.find('div', class_='company').text
            except:
                name = None

            try:
                tick = ticker.find('div', class_='ticker').text
            except:
                tick = None

            if tick == None:
                continue

            try:    
                old_eps = ticker.find('div', class_='estimate').text
                if old_eps == ' - ':
                    old_eps = None
            except:
                old_eps = None

            try:    
                actial_eps = ticker.find('div', class_='actual').text
                if actial_eps == ' - ':
                    actial_eps = None
            except:
                actial_eps = None

            try:    
                actial_dohod = ticker.find('div', class_='revactual').text
                if actial_dohod == ' - ':
                    actial_dohod = None
            except:
                actial_dohod = None

            try:    
                old_dohod = ticker.find('div', class_='revest').text
                if old_dohod == ' - ':
                    old_dohod = None
            except:
                old_dohod = None

            try:
                bcs_url = f"https://bcs-express.ru/kotirovki-i-grafiki/{tick}"
                bcs_src = requests.get(url=bcs_url, headers=headers)
                bcs_soup = BeautifulSoup(bcs_src.text, "html.parser")
                isin = bcs_soup.find_all('div', class_='quote-emitent__data-value')
                isin = isin[-2].text
            except:
                isin = None

            print(actial_eps, actial_dohod, '|', old_eps, old_dohod)
            if (actial_dohod == None) or (actial_eps == None):
                mini_data = {tick:{'eps': actial_eps, 'dohod': actial_dohod}}
                data.update(mini_data)

            # mini_data = {tick:{'eps': actial_eps, 'dohod': actial_dohod}}
            # data.update(mini_data)    
            #print(name,actial_eps,actial_dohod, tick, isin)
    
        print(data)
        print(len(data))
    except:
        pass

def while_true(url, finded):
    try:
        src = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(src.text, "html.parser")
        eps = soup.find('ul', id = finded)
        li = eps.find_all('li')
    except:
        pass
    
    try:
        for ticker in li:
            try:
                name = ticker.find('div', class_='company').text
            except:
                name = ''

            try:
                tick = ticker.find('div', class_='ticker').text
            except:
                tick = None

            if tick == None:
                continue

            try:    
                old_eps = ticker.find('div', class_='actestimate').text
                # actestimate estimate
                if old_eps == ' - ':
                    old_eps = ' '
            except:
                old_eps = ' '

            try:    
                actial_eps = ticker.find('div', class_='actual').text
                if actial_eps == ' - ':
                    actial_eps = ' '
            except:
                actial_eps = None

            try:    
                actial_dohod = ticker.find('div', class_='revactual').text
                if actial_dohod == ' - ':
                    actial_dohod = ' '
            except:
                actial_dohod = ' '

            try:    
                old_dohod = ticker.find('div', class_='actrevest').text
                # actrevest revest
                if old_dohod == ' - ':
                    old_dohod = ' '
            except:
                old_dohod = ' '

            try:
                bcs_url = f"https://bcs-express.ru/kotirovki-i-grafiki/{tick}"
                bcs_src = requests.get(url=bcs_url, headers=headers)
                bcs_soup = BeautifulSoup(bcs_src.text, "html.parser")
                isin = bcs_soup.find_all('div', class_='quote-emitent__data-value')
                isin = isin[-2].text
                url = 'https://www.finam.ru/documents/commissionrates/marginal/ksur'
                long = requests.get(url=url, headers=headers)
                long_soup = BeautifulSoup(long.text, "html.parser")
                longs = long_soup.find('td', text=isin).findNext().text
                if longs == isin:
                    longs = long_soup.find('td', text=isin).findNext().findNext().text
                    shorts = long_soup.find('td', text=isin).findNext().findNext().findNext().text
                else:
                    longs = long_soup.find('td', text=isin).findNext().text
                    shorts = long_soup.find('td', text=isin).findNext().findNext().text
                if longs == '+':
                    long_status = '🔷Бумага доступна в лонг🔷'
                else:
                    long_status = ''
                if shorts == '+':
                    short_status = '🔶Бумага доступна в шорт🔶'
                else:
                    short_status = ''
            except:
                isin = ' '
                long_status = ' '
                short_status = ' '
            

            try:
                eps_start = data[tick]['eps']
                dohod_start = data[tick]['dohod']
                
                if actial_eps != None:
                    print(tick)
                    try:
                        actial_eps, ac = numbers(actial_eps)
                    except:
                        actial_eps = ''
                    print(actial_eps)
                    try:
                        old_eps, ae = numbers(old_eps)
                    except:
                        old_eps = ''
                    print(old_eps)
                    try:
                        actial_dohod, ad = numbers(actial_dohod)
                        
                    except:
                        actial_dohod = ''  
                        ad = ''  
                    print(actial_dohod)
                    try:
                        old_dohod, od = numbers(old_dohod)
                        
                    except:
                        old_dohod = ''
                        od = ''
                    print(old_dohod)
                    
                    try:
                        eps_status = status(old_eps, actial_eps, 'EPS')
                    except:
                        eps_status = ''
                    print(eps_status)

                    try:
                        dohod_status = status(old_dohod, actial_dohod, 'Доход')
                    except:
                        dohod_status = ''
                    print(dohod_status)
                    
                    try:
                        asd = (datetime.fromtimestamp(time.time() +10800,timezone.utc))
                        start_time = (asd.strftime("%H.%M"))
                    except:
                        start_time = ''
                    print(start_time)
                    
                    try:
                        message = f'{name} | {tick}\n{eps_status}\n{dohod_status}\nEPS отчёт/прогноз: {actial_eps}$ / {old_eps}$\nДоход отчёт/прогноз: {actial_dohod}{ad} / {old_dohod}{od}\n⏰{start_time}⏰\n{long_status}\n{short_status}'
                    except:
                        message = 'asd'
                    print(message)
                    async def somefunc():
                        await bot.send_message(1080509959, message)
                        await bot.send_message(760296324, message)
                    if __name__ == '__main__':
                        executor.start(dp, somefunc())
                    print(data[tick])
                    del data[tick]
                    
            except:
                pass
    except:
        pass

            # mini_data = {tick:{'eps': actial_eps, 'dohod': actial_dohod}}
            # data.update(mini_data)    
            #print(name,actial_eps,actial_dohod, tick, isin)

    
    print(len(data))
data = {}
start('https://www.earningswhispers.com/calendar', 'epscalendar')
start('https://www.earningswhispers.com/morecalendar','morecalendar')
while True:
    while_true('https://www.earningswhispers.com/calendar', 'epscalendar')
    while_true('https://www.earningswhispers.com/morecalendar','morecalendar')

    qwersd = (datetime.fromtimestamp(time.time() +12600,timezone.utc))

    sswer = (qwersd.strftime("%H"))
    if sswer == '07':
        time.sleep(3700)
        data = {}
        start('https://www.earningswhispers.com/calendar', 'epscalendar')
        start('https://www.earningswhispers.com/morecalendar','morecalendar')

    print(sswer)