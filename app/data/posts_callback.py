from flask import Blueprint, request

from app.models import Post
from app import get_db_session

blueprint = Blueprint('posts_callback', __name__, template_folder='templates')


@blueprint.route('/callback', methods=['POST'])
def get_new_post():
    """
    Add new post into the database.

    VK CALLBACK API send a json for completed event in group.
    event = new post EXCEPT A SUGGESTED POSTS
    """

    response = request.json
    obj = response['object']
    if obj['post_type'] != 'post':
        return

    session = get_db_session()

    # if post is already in the db --> exit
    if session.query(Post).filter(Post.vk_id == int(obj['id'])).first():
        return
    if 'attachments' not in obj.keys() or \
            sum(map(lambda att: 1 if att['type'] == 'photo' else 0, obj['attachments'])) > 1 \
            or 'photo' not in obj['attachments'][0].keys():
        return

    # create the Post obj. and add it into the db
    post = Post(
        vk_id=obj['id'],
        photo_url=obj['attachments'][0]['photo']['photo_807']
        if 'photo_807' in obj['attachments'][0]['photo'].keys()
        else obj['attachments'][0]['photo']['photo_604']
    )
    session.add(post)
    session.commit()
