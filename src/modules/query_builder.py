from src import db

class QueryBuilder:
    def __init__(self, query_class: tuple, query_args: list):
        self.query = db.session.query(query_class)
        for element in query_args:
            self.query.filter(element[0].__dict__[element[1]] == element[2])

    def execute(self):
        return self.query.all()