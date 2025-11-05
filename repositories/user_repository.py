from models import User
from repositories.base_repository import BaseRepository

from sqlalchemy.orm import joinedload

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    
    def get_all(self):
        return User.query.filter_by(active=True).all()

    def get_all_including_inactive(self):
        return User.query.all()

    # REVISAR PARA APLICAR A LOS DEMAS GETTERS:
    # Se le agrega a la query un joinedload() que permite traer la relacion de
    # rol que hay entre User y UserCredentials, se accede con User.credential.role
    def get_by_id(self, id):
        return User.query.options(joinedload(User.credential)).get_or_404(id)
    
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()