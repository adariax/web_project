def is_admin(vk_id, access_token, group_id):
    from requests import get

    vk_api_url = "https://api.vk.com/method/"
    method = 'groups.get'

    params = {
        'user_id': vk_id,
        'extended': '1',
        'fields': 'is_admin',
        'access_token': access_token,
        'v': '5.3'
    }

    response = get(vk_api_url + method, params=params).json()
    for group in response['response']['items']:
        if group['id'] == group_id:
            return True if group['is_admin'] else False
    return False

