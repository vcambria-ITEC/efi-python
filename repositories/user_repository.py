from models import User, db

class UserRepository:

    def get_all(self):
        return User.query.all()

    def get_by_id(self, id):
        return User.query.get_or_404(id)

    def save(self, user):
        db.session.add(user)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()