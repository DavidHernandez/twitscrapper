import sys
import json
import itertools

import pygsheets
import pcre
from slugify import slugify
from ..models.topic import Topic


class TagUpdater:

    def __init__(self, verbose=False):
        self.GOOGLE_DRIVE_CREDENTIALS_FILE = './data/credentials.json'
        self.DATA_REFERENCE_FILE = 'isglobal.json'
        self.verbose = verbose
        self.topics = list()
        self.data_reference = list()
        self.google_credentials = None

    def __regex_validation(self, tagname, regex):
        try:
            pcre.compile('(?i)'+regex)
        except Exception as e:
            print(tagname, e)

    def __validate(self, tag):
        if tag['shuffle']:
            delimiter = '.*?' if '.*?' in tag['regex'] else '.*'
            perms = itertools.permutations(tag['regex'].split(delimiter))
            for perm in perms:
                self.__regex_validation(tag['tag'], delimiter.join(perm))
        else:
            self.__regex_validation(tag['tag'], tag['regex'])

    def load_data_reference(self):
        with open('./data/' + self.DATA_REFERENCE_FILE, 'r') as data_reference_file:
            self.data_reference = json.load(data_reference_file)

    def get_knowledge_base(self):
        return self.DATA_REFERENCE_FILE.split('.')[0]

    def load_google_credentials(self):
        self.google_credentials = pygsheets.authorize(
                service_account_file=self.GOOGLE_DRIVE_CREDENTIALS_FILE
                )

    def load_topics(self):
        for data_reference_item in self.data_reference:
            if self.verbose:
                print("[EXTRACT] {}".format(data_reference_item['name']))
            filename = data_reference_item['filename']
            filesheet = self.google_credentials.open(filename)
            wks = filesheet.sheet1
            topic = data_reference_item.copy()
            del topic['filename']
            topic['_id'] = slugify(topic['shortname'].lower())
            topic['tags'] = []
            data = wks.get_values(grange=pygsheets.GridRange(worksheet=wks, start=None, end=None))
            for row in data[1:]:
                if row[0] == '' and row[1] == '' and row[2] == '' and row[3] == '':
                    continue
                tag = {
                        'regex': row[3],
                        'tag': row[2],
                        'subtopic': row[1],
                        'shuffle': bool(int(row[0]))
                        }
                self.__validate(tag)
                topic['knowledgebase'] = filename
                topic['public'] = True
                topic['tags'].append(tag)
            self.topics.append(topic)

    def create_topics(self):
        for topic in self.topics:
            Topic.from_json(topic)

    def run(self):
        self.load_data_reference()
        self.load_google_credentials()
        self.load_topics()
        self.create_topics()

    @staticmethod
    def execute():
      print('Initializing')
      extractor = TagUpdater(verbose=True)
      print('Executing')
      extractor.run()
      print('Done')
