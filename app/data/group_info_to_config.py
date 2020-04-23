from requests import get


def get_info(config):
    """
    :param config: app's config

    :return: values for config including group's name & screen name

    Values getting from req to the VK API.
    """

    vk_api_url = "https://api.vk.com/method/"

    params = {'group_ids': config['VK_GROUP_ID'][1:],
              'access_token': config['ACCESS_TOKEN'],
              'v': '5.2'}

    # getting info
    group_info = get(vk_api_url + 'groups.getById', params=params).json()['response'][0]

    vk_group_name = group_info['name']
    vk_group_screen_name = group_info['screen_name']

    return vk_group_name, vk_group_screen_name
