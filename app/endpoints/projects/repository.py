from core.db.models import Project
from core.db.repository import DBRepository


class ProjectRepository(DBRepository):
    db_model = Project


projects_repository = ProjectRepository()
