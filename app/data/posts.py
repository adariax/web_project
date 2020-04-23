import requests
from app import app

VK_API_URL = "https://api.vk.com/method/"


def get_attachment(access_token, data, group_id, user_id):
    """
    :param access_token: user's access token
    :param data: bytes of img

    :return: str of attachment info for pin to the post
    """

    # getting info of the loading server
    upload_server = requests.get(VK_API_URL + 'photos.getWallUploadServer', params={
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.103'
    }).json()

    # get load attr
    photo_upload = requests.post(upload_server['response']['upload_url'],
                                 files={'photo': data}).json()
    # getting attachment info
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


def get_suggests(access_token):
    """
    :param access_token: access token for getting sug. posts for admin
    """

    # checking if items is empty --> there no posts
    is_empty = lambda items: False if items else True

    items, offset = None, 0
    posts = []

    while True:
        params = {'owner_id': app.config['VK_GROUP_ID'],
                  'extended': '1',
                  'count': '100',
                  'filter': 'suggests',
                  'offset': offset,
                  'access_token': access_token,
                  'v': '5.2'}
        items = requests.get(VK_API_URL + 'wall.get', params=params).json()['response']['items']

        # if no posts --> exit the func & return the list
        if is_empty(items):
            return posts

        # getting posts info
        for item in items:
            if 'attachments' not in item.keys():
                continue
            if 'photo' not in item['attachments'][0].keys():
                continue
            post = {
                'vk_id': item['id'],
                'photo_url': item['attachments'][0]['photo']['photo_807']
                if 'photo_807' in item['attachments'][0]['photo'].keys()
                else item['attachments'][0]['photo']['photo_604']
            }
            posts.append(post)

        offset += 100
