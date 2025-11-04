from repositories.stats_repository import StatsRepository
from marshmallow import ValidationError

class StatsService:

    def __init__(self):
        self.repo = StatsRepository()

    
    def get_stats(self, current_user_role):


        stats_data = {
            "total_posts": self.repo.count_total_posts(),
            "total_comments": self.repo.count_total_comments(),
            "total_users": self.repo.count_total_users()
        }

        if current_user_role == 'admin':
            stats_data["posts_last_week"] = self.repo.count_posts_last_week()

        return stats_data