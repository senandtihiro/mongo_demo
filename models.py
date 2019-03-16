from pymongo import MongoClient


client = MongoClient('localhost', 27017)    #Configure the connection to the database
mongodb = client.prompts    #Select the database


class Model(object):
    def __str__(self):
        class_name = self.__class__.__name__
        properties = (u'{0} = ({1})'.format(k, v) for k, v in self.__dict__.items())
        r = u'\n<{0}:\n  {1}\n>'.format(class_name, u'\n  '.join(properties))
        return r

    def save(self):
        '''
        保存数据到 mongo
        '''
        name = self.__class__.__name__
        mongodb[name].save(self.__dict__)


class DataType(Model):
    light = []
    standard = []

    def __init__(self, form):
        self.light = form.get('light')
        self.standard = form.get('standard')


class Prompt(Model):
    id = 0
    title = ''
    description = ''
    type = 0
    play_beep = False
    show_hmi = False
    barge_in = False
    data = None
    simple_data = None
    replace = {}

    def __init__(self, form):
        super(Prompt, self).__init__()
        self.id = 0
        self.title = form.get('title')
        self.description = form.get('description')
        self.type = form.get('type')
        self.play_beep = form.get('play_beep')
        self.show_hmi = form.get('show_hmi')
        self.barge_in = form.get('barge_in')
