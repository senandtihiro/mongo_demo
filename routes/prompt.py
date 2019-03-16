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


@main.route('/modify', methods=['POST'])
def modify():
    form = request.form.to_dict()
    pid = form.get('id')
    mongodb['Prompt'].update({"id": pid}, {"$set": form})
    return redirect(url_for('.index'))


@main.route('/edit/<id>')
def edit(id):
    _p = mongodb['Prompt'].find_one({'id': str(id)})
    return render_template('prompt_edit.html', prompt=_p)