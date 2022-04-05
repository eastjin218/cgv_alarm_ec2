import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import telegram

bot = telegram.Bot(token = '1287968679:AAG79uzbYMf1mFsOLD4xa_uQAfzH8DBkRKo')
url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=204&theatercode=0023&date=20200527'

def job_function():
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    fordx = soup.select_one('span.forDX')
    if(fordx):
        fordx = fordx.find_parent('div', class_='col-times')
        title = fordx.select_one('div.info-movie > a > strong').text.strip()
        # print(title +'4DX 예매가 열렸습니다.')
        bot.sendMessage(chat_id = 1170137075, text = title +'4DX 예매가 열렸습니다.')
        sched.pause()

sched= BlockingScheduler()
sched.add_job(job_function, 'interval', seconds=10)
sched.start()
