from flask import jsonify, Blueprint, request, make_response
from flask_login import login_required, current_user
from flask_restful import Resource
from app.data.parser import fav_post_parser as parser

from app.models import Post, User
from app import get_db_session, app
from app.data.posts import get_attachment, get_suggests

from datetime import datetime
from pytz import timezone
from base64 import b64decode


class FavPost(Resource):
    @login_required
    def get(self):
        """
        :return: object with list of fav posts
        """

        user_id = current_user.id
        session = get_db_session()
        user = session.query(User).filter(User.id == user_id).first()
        posts = user.favors
        return jsonify({'posts': [post.to_dict(only=('id', 'vk_id', 'photo_url'))
                                  for post in posts[::-1]]})

    @login_required
    def post(self):
        """
        Getting obj with group id from the request;
        Getting current user's id;

        Add to the favorites table association user-post.
        """

        post_id = parser.parse_args()['post_id']
        user_id = current_user.id
        session = get_db_session()
        user = session.query(User).filter(User.id == user_id).first()
        post = session.query(Post).filter(Post.id == post_id).first()
        user.favors.append(post)
        session.commit()

    @login_required
    def delete(self):
        """
        Getting obj with group id from the request;
        Getting current user's id;

        Delete from favorites table association user-post with.
        """

        post_id = parser.parse_args()['post_id']
        user_id = current_user.id
        session = get_db_session()
        user = session.query(User).filter(User.id == user_id).first()
        post = session.query(Post).filter(Post.id == post_id).first()
        user.favors.remove(post)
        session.commit()


blueprint = Blueprint('posts_rest_api', __name__, template_folder='templates')


@blueprint.route('/api/posts')
def get_posts():
    """
    :return: obj with list of posts

    Type of posts is selected based on the type of page, from which the request was received.
    """

    session = get_db_session()
    post_type = request.args.get('type')

    posts = []
    if post_type == 'all':
        posts = session.query(Post).all()
    elif post_type == 'fav':
        posts = session.query(User).filter(User.id == current_user.id).first().favors
    elif post_type == 'sug':
        return jsonify({'posts': get_suggests(current_user.access_token)})
    return jsonify({'posts': [post.to_dict(only=('id', 'vk_id', 'photo_url'))
                              for post in posts[::-1]]})


@blueprint.route('/api/posts/unixtime_<date>_<time>_<tz>')
def get_unix(date, time, tz):
    """
    :param date: date in format DD-MM-YYYY
    :param time: time in format MM-HH
    :param tz: time zone - delta of GTM // For Barnaul it's 7, for Silicon Valley it's -7
    :return: obj with str of unixtime

    If incorrect format --> handler return 400 response.
    """

    try:
        hours, minutes = map(int, time.split(':'))
        day, month, year = map(int, date.split('.'))
        unix = datetime(year, month, day, hours, minutes, 0,
                        tzinfo=timezone("UTC")).timestamp() - float(tz) * 3600
        return jsonify({'unixtime': int(unix)})
    except Exception:
        return make_response({'error': 'bad request'}, 400)


@blueprint.route('/api/posts/picture', methods=['POST'])
@login_required
def get_picture():
    """
    :return: obj with str of attachment
    """

    data_img = request.form.get('image').split(',')
    img_format = data_img[0].split('/')[1].split(';')[0]
    img_content = b64decode(data_img[1])
    file_path = f"app/static/img/file_on_load/load.{img_format}"
    with open(file_path, 'wb') as img:
        img.write(img_content)

    return jsonify({'attachment': get_attachment(current_user.access_token,
                                                 data=open(file_path, 'rb'),
                                                 group_id=app.config['VK_GROUP_ID'][1:],
                                                 user_id=current_user.vk_domain)})
