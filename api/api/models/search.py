from ..config import db


class Search(db.Document):
    id = db.StringField(db_field='id', primary_key=True)
    text = db.StringField()
