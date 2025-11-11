from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from services.stats_service import StatsService
from utils.decorators import role_required

blp = Blueprint("Stats", "stats", url_prefix="/api/stats")

@blp.route("/")
class StatsResource(MethodView):
    def __init__(self):
        self.service = StatsService()

    @jwt_required()
    @role_required("admin", "moderator")
    def get(self):
        role = get_jwt().get("role")
        stats = self.service.get_stats(role)
        return stats, 200
