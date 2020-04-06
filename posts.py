def load_posts():
    from requests import get
    from app import get_db_session
    from app.models import Post
    import app

    ACCESS_TOKEN = app.app.config['VK_ACCESS_TOKEN']
    VK_API_URL = "https://api.vk.com/method/"
    METHOD = 'wall.get'

    is_empty = lambda items: False if items else True

    session = get_db_session()
    vk_ids = list(map(lambda vk_id: vk_id[0], session.query(Post.vk_id)))
    items, offset = None, 0
    while True:
        params = {'owner_id': '-112055138',
                  'extended': '1',
                  'count': '100',
                  'filter': 'all',
                  'offset': offset,
                  'access_token': ACCESS_TOKEN,
                  'v': '5.2'}
        items = get(VK_API_URL + METHOD, params=params).json()['response']['items']

        if is_empty(items):
            session.commit()
            print('Posts were successfully added into a database')
            return
        for item in items:
            if item['id'] in vk_ids:
                session.commit()
                print('Post was successfully added into a database')
                return
            if 'attachments' not in item.keys():
                continue
            if sum(map(lambda att: 1 if att['type'] == 'photo' else 0, item['attachments'])) > 1 \
                    or 'photo' not in item['attachments'][0].keys():
                continue
            post = Post(
                vk_id=item['id'],
                description=item['text'],
                photo_url=item['attachments'][0]['photo']['photo_807']
                if 'photo_807' in item['attachments'][0]['photo'].keys()
                else item['attachments'][0]['photo']['photo_604']
            )
            session.add(post)

        offset += 100


if __name__ == '__main__':
    load_posts()
