import vk_api
import sys
import requests
import pandas as pd
from config import *
from constants import Wishes
from datetime import datetime, timedelta
import time
import re


def vk_auth(login, access_token):
    session = vk_api.VkApi(login=login, token=access_token)

    try:
        session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        sys.exit()

    return session.get_api()


def get_photo_attachments(vk, photo_path, group_id):
    link = vk.photos.getWallUploadServer(group_id=group_id)
    upload_url = link['upload_url']
    r = requests.post(upload_url, files={'photo': open(photo_path, 'rb')})

    answer = r.json()

    wall_photo = vk.photos.saveWallPhoto(
        photo=answer['photo'],
        server=answer['server'],
        hash=answer['hash'],
        group_id=group_id,
    )

    return 'photo{}_{}'.format(wall_photo[0]['owner_id'], wall_photo[0]['id'])


def get_vk_id(vk_url):
    return vk_url[7:]


def get_spreadsheet(from_path):
    spreadsheet = pd.read_csv(from_path)

    result = []
    for i in range(1, len(spreadsheet['Unnamed: 0'])):
        row = spreadsheet.loc[i, :]

        if today(str(row[5])):
            buf = dict()
            buf['name'] = str(row[0])
            buf['date'] = str(row[5])
            buf['id'] = get_vk_id(str(row[8]))
            buf['photo'] = str(row[17])
            result.append(buf)

    return result


def today(date):
    vals = date.split('.')
    day, month = int(vals[0]), int(vals[1])
    d = datetime.now() + timedelta(days=2)
    return d.month == month and d.day == day


def get_current(mem_list):
    result = []
    for member in mem_list:
        if today(member['date']):
            result.append(member)
    return result


def make_name(name):
    tokens = name.split(' ')
    if tokens[1][0] == '(':
        return '{0} {1}'.format(tokens[2], tokens[0])
    else:
        return '{0} {1}'.format(tokens[1], tokens[0])


def make_message(item):
    w = Wishes()
    name = make_name(item['name'])
    message = 'Хе-хей!\n\nА сегодня свой день рождения празднует @{0} ({1})! От имени всего {2} мы желаем тебе {3}, {4} и {5}. ' \
              '{6} {7}\n\nТвой Фотон.'.format(item['id'], name, w.get_from(), w.get_common(), w.get_study(), w.get_camp(),
                               w.get_state(), w.get_hb())
    return message


def need_to_post(item, vk):
    posts = vk.wall.get(owner_id=-GROUP_ID, filter='postponed')

    if datetime.now().hour != 12:
        return False

    for post in posts['items']:
        if post['text'].find(make_name(item['name'])) > 0:
            return False
    return True


def get_photo(photo_url):
    return re.search(r'photo[0123456789-]+_[0123456789-]+', photo_url).group(0)


def post_congratulation(item, vk):
    attachment_photo = get_photo(get_photo(item['photo']))

    d = datetime.now() + timedelta(days=2)
    unix_time = int(time.mktime(d.timetuple()))

    message = make_message(item)
    result = vk.wall.post(
        owner_id=-GROUP_ID,
        from_group=1,
        message=message,
        attachments=attachment_photo,
        publish_date=unix_time
    )

    return result


def make_step():
    mem_list = get_spreadsheet(CSV_URL)
    today_list = get_current(mem_list)

    vk = vk_auth(LOGIN, ACCESS_TOKEN)

    result = []
    for item in today_list:
        if need_to_post(item, vk):
            result.append(post_congratulation(item, vk))

    send_report(result, vk)


def send_report(result, vk):
    text = '(Сообщение от бота)\nПост с поздравлнеием в отложке'.format(len(result))
    if len(result) > 0:
        vk.messages.send(peer_id='2000000307', message=text)
    # print(result)

