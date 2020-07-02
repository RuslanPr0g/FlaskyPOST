import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import app, mail


def save_image_for_user(_image):
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(_image.filename)
    img_fn = rand_hex + f_ext
    img_path = os.path.join(app.root_path, 'static/profile_images', img_fn)

    output_size = (125, 125)
    i = Image.open(_image)
    i.thumbnail(output_size)
    i.save(img_path)

    return img_fn


def send_token_by_email(user):
    token = user.get_reset_token()
    message = Message('Reset Password Request.',
                      sender='theruslanrudenko1992@gmail.com', recipients=[user.email])
    message.body = f''' 
Reset Password Link: {url_for('password_reset', token=token, _external=True)}
If you haven't made this request, just ignore it.
'''
    mail.send(message)
