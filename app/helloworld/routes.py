
from glob import escape

from flask import render_template, request

from . import helloworld

# Routing examples
@helloworld.route('/', methods=['GET'])
def index():
    return 'Resource not found!'

@helloworld.route('/helloworld', methods=['GET'])
def hello_world():
    return 'hello world!'

# Variable Rules
@helloworld.route('/user/<username>', methods=['GET'])
def show_user_profile(username):
    return f'User: {username}'

@helloworld.route('/post/<int:post_id>', methods=['POST'])
def show_post(post_id):
    return f'Post: {post_id}'

@helloworld.route('/path/<path:subpath>')
def show_subpath(subpath): 
    return f'Subpath: {escape(subpath)}'

# Unique URLs/Redirection Behavior
@helloworld.route('/projects/')
def projects():
    return 'The project page'

@helloworld.route('/about')
def about():
    return 'The about page'

# Accessing Request Data

## Accessing parameters in the URL(?key=value)
@helloworld.route('/param', methods=['GET'])
def param_from_url():
    val1 = request.args.get('k1')
    val2 = request.args.get('k2')
    return f'k1={val1}&k2={val2}'

## Accessing form data 
@helloworld.route('/request/formdata', methods=['POST'])
def formdata():
    val1 = request.form['k1']
    val2 = request.form['k2']
    return f'k1={val1}&k2={val2}'

## Accessing raw data(json)
@helloworld.route('/request/raw/json', methods=['POST'])
def rawdata():
    json = request.get_json()
    return {
        'a': 'a',
        'b': 'b'
    }

## Accessing header data
@helloworld.route('/request/header')
def headerdata():
    val1 = request.headers.get('k1')
    val2 = request.headers.get('k2')
    return f'k1={val1}&k2={val2}'

## File Uploads
@helloworld.route('/request/fileuploads', methods=['POST'])
def fileuploads():
    filepath = './uploaded_file.txt'
    f = request.files['file']
    f.save(filepath)
    with(open(filepath)) as f:
        filelines = f.readlines()
    return filelines

@helloworld.route('/request/404', methods = ['GET'])
def get404():
    return "", 404


@helloworld.route('/template/hello', methods = ['GET'])
def render_hello():
    return render_template('./hello.html', name='xiaosi')

@helloworld.route('/template/hello/<name>', methods = ['GET'])
def render_hello_path_variable(name):
    return render_template('./hello.html', name=name)