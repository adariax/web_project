def is_admin(vk_id, access_token):
    from requests import get
    from app import app

    VK_API_URL = "https://api.vk.com/method/"
    METHOD = 'groups.get'
    GROUP_ID = int(app.config['VK_GROUP_ID'][1:])

    params = {
        'user_id': vk_id,
        'extended': '1',
        'fields': 'is_admin',
        'access_token': access_token,
        'v': '5.3'
    }

    response = get(VK_API_URL + METHOD, params=params).json()
    for group in response['response']['items']:
        if group['id'] == GROUP_ID:
            return True if group['is_admin'] else False
    return False

