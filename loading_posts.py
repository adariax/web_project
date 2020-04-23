def load_posts(access_token, group_id, session):
    """
    :param access_token: app's access token
    :param group_id: group id for getting posts
    :param session: db session for loading posts

    Getting ALL wall posts from current group.
    """

    from requests import get
    from app.models import Post

    vk_api_url = "https://api.vk.com/method/"
    method = 'wall.get'

    vk_ids = list(map(lambda vk_id: vk_id[0], session.query(Post.vk_id)))

    # checking if items is empty --> there no posts
    is_empty = lambda items: False if items else True

    items, offset = None, 0
    posts = []

    while True:
        params = {'owner_id': group_id,
                  'extended': '1',
                  'count': '100',
                  'filter': 'all',
                  'offset': offset,
                  'access_token': access_token,
                  'v': '5.2'}
        items = get(vk_api_url + method, params=params).json()['response']['items']

        # if no posts --> adding Posts into the db & exit the func
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

            # app needs only non-text posts
            if 'attachments' not in item.keys():
                continue

            # with 1 picture
            if sum(map(lambda att: 1 if att['type'] == 'photo' else 0, item['attachments'])) > 1 \
                    or 'photo' not in item['attachments'][0].keys():
                continue

            # create Post obj.
            post = Post(
                vk_id=item['id'],
                photo_url=item['attachments'][0]['photo']['photo_807']
                if 'photo_807' in item['attachments'][0]['photo'].keys()
                else item['attachments'][0]['photo']['photo_604']
            )
            posts.append(post)

        offset += 100
