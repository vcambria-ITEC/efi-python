from models import Post, Category, db

class PostRepository:

    def get_all(self):
        return Post.query.all()

    def get_by_id(self, id):
        return Post.query.get_or_404(id)

    def save(self, post):
        db.session.add(post)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, post):
        db.session.delete(post)
        db.session.commit()