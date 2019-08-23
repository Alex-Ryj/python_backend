from flask import send_file
from io import StringIO


def echo_get(message):
    # do something
    return 'You send the message: {}'.format(message), 200


def post_example(body):
    return 'posted empty'


def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
