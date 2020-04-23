from requests import get


def is_admin(vk_id, access_token, group_id):
    """
    :param vk_id: user's id
    :param access_token: access token for users actions
    :param group_id: group id for checking

    :return: True - user is admin, False - user is not
    """

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

