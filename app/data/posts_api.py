from flask import jsonify, Blueprint, request, make_response
from flask_login import login_required, current_user

from app.models import Post
from app import get_db_session, app
from app.data.posts import get_attachment

blueprint = Blueprint('posts_rest_api', __name__, template_folder='templates')


@blueprint.route('/api/posts')
def get_posts():
    session = get_db_session()
    posts = session.query(Post).all()
    return jsonify({'posts': [post.to_dict(only=('id', 'vk_id', 'photo_url'))
                              for post in posts[::-1]]})


@blueprint.route('/api/posts/unixtime_<date>_<time>_<tz>')
@login_required
def get_unix(date, time, tz):
    import datetime
    import pytz

    try:
        hours, minutes = map(int, time.split(':'))
        day, month, year = map(int, date.split('.'))
        unix = datetime.datetime(year, month, day, hours, minutes, 0,
                                 tzinfo=pytz.timezone("UTC")).timestamp() - float(tz) * 3600
        return jsonify({'unixtime': int(unix)})
    except Exception:
        return make_response({'error': 'bad request'}, 400)


@blueprint.route('/api/posts/picture', methods=['POST'])
@login_required
def get_picture():
    import base64

    data_img = request.form.get('image').split(',')
    img_format = data_img[0].split('/')[1].split(';')[0]
    img_content = base64.b64decode(data_img[1])
    file_path = f"app/static/img/file_on_load/load.{img_format}"
    with open(file_path, 'wb') as img:
        img.write(img_content)

    return jsonify({'attachment': get_attachment(current_user.access_token,
                                                 data=open(file_path, 'rb'),
                                                 group_id=app.config['VK_GROUP_ID'][1:],
                                                 user_id=current_user.vk_domain)})
