from models import db

class BaseRepository:
    """
    This repository is used to handle common database operations.
    We've implemented it to follow DRY principle.
    (Don't Repeat Yourself).
    """
    def __init__(self):
        self.db_session = db.session
    
    def save(self, obj):
        self.db_session.add(obj)

    def commit(self):
        self.db_session.commit()

    def rollback(self):
        self.db_session.rollback()

    def flush(self):
        self.db_session.flush()