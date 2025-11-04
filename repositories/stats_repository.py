from models import db, Post, Comment, User
from datetime import datetime, timedelta
import pytz

class StatsRepository:

    def __init__(self):
        self.one_week_ago = datetime.utcnow() - timedelta(days=7)

    def count_total_posts(self):

        return Post.query.filter_by(is_published=True).count()
    
    def count_total_comments(self):

        return Comment.query.filter_by(is_visible=True).count()
    
    def count_total_users(self):

        return User.query.filter_by(is_active=True).count()
    
    def count_posts_last_week(self):
        
        return Post.query.filter(
            Post.created_at >= self.one_week_ago
        ).count()