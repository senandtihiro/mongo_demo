from . import *

main = Blueprint('blog', __name__)


@main.route("/")
def hello():
    # print('666666666666666')
    return "Hello World!"