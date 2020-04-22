def get_info(config):
    from requests import get

    VK_API_URL = "https://api.vk.com/method/"

    params = {'group_ids': config['VK_GROUP_ID'][1:],
              'access_token': config['ACCESS_TOKEN'],
              'v': '5.2'}
    group_info = get(VK_API_URL + 'groups.getById', params=params).json()['response'][0]

    vk_group_name = group_info['name']
    vk_group_screen_name = group_info['screen_name']

    return [vk_group_name, vk_group_screen_name]
