from flask import Flask
from flask_script import Manager
from pymongo import MongoClient


app = Flask(__name__)
manager = Manager(app)


def register_routes(app):
    from routes.prompt import main as routes_prompt
    app.register_blueprint(routes_prompt)


def configure_app():
    app.secret_key = 'secret key'
    register_routes(app)


def configured_app():
    configure_app()
    return app


@manager.command
def server():
    '''
    用flask-script可以使用我们指定的命令来运行app
    这里取名server
    那么我们运行app时的命令就是：python3 app.py server
    :return:
    '''
    print('server run')
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5001,
    )
    app.run(**config)



if __name__ == '__main__':
    manager.run()