import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbgenie

db.users.delete_one({'name': '덤블도어'})

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

tracks = soup.select('div.newest-list > div > table > tbody > tr')

for track in tracks:
    # 제목 경로
    # body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
    # 순위 경로
    # body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
    # 가수 경로
    # body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
    title = track.select_one('td.info > a.title.ellipsis')
    title_text = title.text.strip()

    num = track.select_one('td.number')
    num_text = num.text[0:2].strip()

    artist = track.select_one('td.info > a.artist.ellipsis')
    artist_text = artist.text

    item = {
        'rank':num_text,
        'title':title_text,
        'artist':artist_text,
    }
    print(item)
    db.genie.insert_one(item)