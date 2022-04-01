from ..config import db

class List(db.Document):
    id = db.StringField(db_field='_id', primary_key=True)
    owner_id = db.StringField()
    name = db.StringField()
    description = db.StringField()
    member_list = db.ListField(db.StringField(), default=list)
    member_count = db.IntField()
    follower_count = db.IntField()
    raw = db.DynamicField()

    def add_member(self, user_id):
        self.member_list.append(user_id)

    @staticmethod
    def from_json(json):
        new_list = List(
            id=str(json['id']),
            owner_id=str(json['owner_id']),
            name=json['name'],
            description=json['description'],
            member_count=json['member_count'],
            follower_count=json['follower_count'],
            raw=json
        )

        new_list.save()
        return new_list
