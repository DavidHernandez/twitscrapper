from ..config import db

class List(db.Document):
    id = db.IntField(db_field='id', primary_key=True)
    name = db.StringField()
    owner_list = db.StringField()
    raw = db.DynamicField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_json(json):
        listMembership = List(
            id=json['id'],
            name=json['name'],
            owner_list= json['owner_list'],
            raw=json
        )

        listMembership.save()
        return listMembership
