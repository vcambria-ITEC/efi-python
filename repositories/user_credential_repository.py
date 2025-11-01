from models import UserCredential, db

class UserCredentialRepository:

    def get_all(self):
        return UserCredential.query.all()

    def get_by_id(self, id):
        return UserCredential.query.get_or_404(id)

    def save(self, user_credential):
        db.session.add(user_credential)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, user_credential):
        db.session.delete(user_credential)
        db.session.commit()