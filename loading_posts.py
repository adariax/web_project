def load_posts():
    from requests import get
    from app import get_db_session
    from app.models import Post
    from app import app

    ACCESS_TOKEN = app.config['ACCESS_TOKEN']
    VK_GROUP_ID = app.config['VK_GROUP_ID']
    VK_API_URL = "https://api.vk.com/method/"
    METHOD = 'wall.get'

    is_empty = lambda items: False if items else True

    session = get_db_session()
    vk_ids = list(map(lambda vk_id: vk_id[0], session.query(Post.vk_id)))
    items, offset = None, 0
    posts = []

    while True:
        params = {'owner_id': VK_GROUP_ID,
                  'extended': '1',
                  'count': '100',
                  'filter': 'all',
                  'offset': offset,
                  'access_token': ACCESS_TOKEN,
                  'v': '5.2'}
        items = get(VK_API_URL + METHOD, params=params).json()['response']['items']

        if is_empty(items):
            for post in posts[::-1]:
                session.add(post)
            session.commit()
            print('Posts were successfully added into a database')
            return
        for item in items:
            if item['id'] in vk_ids:
                session.commit()
                return
            if 'attachments' not in item.keys():
                continue
            if sum(map(lambda att: 1 if att['type'] == 'photo' else 0, item['attachments'])) > 1 \
                    or 'photo' not in item['attachments'][0].keys():
                continue
            post = Post(
                vk_id=item['id'],
                photo_url=item['attachments'][0]['photo']['photo_807']
                if 'photo_807' in item['attachments'][0]['photo'].keys()
                else item['attachments'][0]['photo']['photo_604']
            )
            posts.append(post)

        offset += 100
