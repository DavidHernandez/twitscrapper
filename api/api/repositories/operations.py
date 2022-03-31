from ..models.operation import Operation

class Operations():

    @staticmethod
    def by_query(query):
        return Operation.objects(__raw__=query)

    @staticmethod
    def by_command_type(command, limit=None):
        db_query = Operation.objects(command=command, execution_date__exists=False)

        if limit:
            db_query.limit(limit)

        return db_query

    @staticmethod
    def get(identifier):
        return Operation.objects(id=identifier).first()

    @staticmethod
    def get_unfinished(operations):
        return Operation.objects(id__in=operations, execution_date__exists=False)
