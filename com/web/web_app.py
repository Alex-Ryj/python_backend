from flask import Flask
import properties as props
from com.amazon.amazon_api import ProductAPI

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id