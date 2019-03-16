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


@main.route('/detail/<id>')
def detail(id):
    _p = mongodb['Prompt'].find_one({'id': str(id)})
    return render_template('prompt_detail.html', p=_p)


@main.route('/data_add', methods=['POST'])
def data_add():
    '''
    data是一个列表类型，应该每次添加一条，
    那么需要先将data的值拿出来再append一条进去之后再update
    :return:
    '''
    id = request.form.get('id')
    _p = mongodb['Prompt'].find_one({'id': str(id)})
    # 为prompt 添加一个字段data
    # db.collection.update({}, {$set: {otherkey: ‘otherval’}}, {multi: 1})
    new_data = request.form.get('content')
    print('debug new_data:', new_data)

    # 根据某个id值查找这条记录中的其他字段的值
    old_data = mongodb['Prompt'].find_one({'id': str(id)}, {'data': 1})
    first_add_data = 'data' not in list(old_data)
    if first_add_data:
        old_data = []
    else:
        # print('debug old_data:', old_data)
        # old_data: {'_id': ObjectId('5c8cabbc8c9592d73d0ca176'), 'data': ['hahaha']}
        old_data = old_data.get('data')
    old_data.append(new_data)

    # 最后执行更新，更新的命令如下
    # mongodb['Prompt'].update({'id': str(id)}, {'$set': {'data': data}})
    mongodb['Prompt'].update({'id': str(id)}, {'$set': {'data': old_data}})
    return render_template('prompt_detail.html', p=_p)