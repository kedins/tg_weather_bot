import telebot
import requests
from bs4 import BeautifulSoup

token = '1352940580:AAGSG9ap8m_rH0b4BklRSIcylzDO2gJWkqQ'
URL = "https://sinoptik.com.ru/погода-челябинск/10-дней"
bot = telebot.TeleBot(token)


def get_html(url):
    r = requests.get(url)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    today_temp = soup.find('div', class_='weather__content_tab')
    day_of_week = today_temp.find('p', class_='weather__content_tab-day').get_text(strip=True)
    date_day = today_temp.find('p', class_='weather__content_tab-date').get_text(strip=True)
    date_month = today_temp.find('p', class_='weather__content_tab-month').get_text(strip=True)
    weather_disc = soup.find('div', class_='weather__article_description-text').get_text(strip=True)
    temps_find = today_temp.find('div', class_='weather__content_tab-temperature')
    temps = temps_find.findAll('b')
    min_temp = temps[0].get_text()
    max_temp = temps[1].get_text()
    return f"""Сегодня {day_of_week}, {date_day} {date_month}
Минимальная температура: {min_temp} Максимальная температура: {max_temp}
{weather_disc}"""


@bot.message_handler(commands=['start', 'help'])
def main(message):
    html = get_html(URL)
    bot.send_message(message.chat.id, get_content(html.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
