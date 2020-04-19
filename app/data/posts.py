VK_API_URL = "https://api.vk.com/method/"


def get_attachment(access_token, data, group_id, user_id):
    import requests

    upload_server = requests.get(VK_API_URL + 'photos.getWallUploadServer', params={
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.103'
    }).json()

    photo_upload = requests.post(upload_server['response']['upload_url'],
                                 files={'photo': data}).json()
    photo = requests.get(VK_API_URL + 'photos.saveWallPhoto', params={
        'user_id': user_id,
        'group_id': group_id,
        'photo': photo_upload['photo'],
        'server': photo_upload['server'],
        'hash': photo_upload['hash'],
        'access_token': access_token,
        'v': '5.103'
    }).json()

    return f"photo{photo['response'][0]['owner_id']}_{photo['response'][0]['id']}"


# from datetime import datetime, timezone, tzinfo
# from tzlocal import get_localzone
# import pytz
# inp = datetime(2020, 4, 19, 22, datetime.now().minute, datetime.now().second, datetime.now().microsecond)
# serv = datetime.now()
# delta = str(serv - inp)
# delta = delta.split(':')[0] if 'day' not in delta else f"-{delta.split(', ')[1].split(':')[0]}"
# print(delta)