from sqlalchemy.orm import Session


class BaseRepository:

    def __init__(self, session):
        self.session = session
