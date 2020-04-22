def get_info(config):
    from requests import get

    new_congig = config
    VK_API_URL = "https://api.vk.com/method/"

    params = {'group_ids': config['VK_GROUP_ID'][1:],
              'access_token': config['ACCESS_TOKEN'],
              'v': '5.2'}
    group_info = get(VK_API_URL + 'groups.getById', params=params).json()['response'][0]

    VK_GROUP_NAME = group_info['name']
    VK_GROUP_SCREEN_NAME = group_info['screen_name']

    return [VK_GROUP_NAME, VK_GROUP_SCREEN_NAME]
