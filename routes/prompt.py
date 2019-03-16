from . import *
from models import Prompt

main = Blueprint('prompt', __name__)


@main.route("/")
def index():
    prompts = mongodb['Prompt'].find()
    return render_template('prompt.html', prompts=prompts)


@main.route("/add", methods=['POST'])
def add():
    print('add called')
    form = request.form
    p = Prompt(form)
    count = mongodb['Prompt'].count()
    p.id = str(count + 1)
    p.save()
    return redirect(url_for('.index'))



@main.route('/delete/<string:title>')
def delete(title):
    print('delete called')
    mongodb['Prompt'].remove({'title': title})
    return redirect(url_for('.index'))
