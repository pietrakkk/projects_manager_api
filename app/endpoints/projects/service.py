import json
from typing import Any

from core.db.config import AsyncSessionLocal
from core.db.models import Project, AreaOfInterest
from endpoints.projects.repository import projects_repository
from endpoints.projects.schema import ProjectCreate, ProjectListResponse
from geoalchemy2.functions import ST_AsGeoJSON
from shapely.geometry import shape
from shapely.wkb import dumps as wkb_dumps
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound


class ProjectService:
    def __init__(self, project_repository):
        self.repository = project_repository

    async def create_project(self, payload: ProjectCreate, file_content: dict[str, Any], file_name: str) -> Project:
        geometry = shape(file_content['geometry'])
        wkb_geometry = wkb_dumps(geometry, hex=True)
        new_file = AreaOfInterest(geometry=wkb_geometry, file_name=file_name)
        project = Project(
            area_of_interest=new_file,
            name=payload.name,
            start_date=payload.start_date,
            end_date=payload.end_date,
            description=payload.description
        )

        return await self.repository.add(project)

    @staticmethod
    async def get_project(project_id: str) -> Project:
        async with AsyncSessionLocal() as session:
            results = (
                select(
                    Project,
                    func.json_build_object(
                        'file_name', AreaOfInterest.file_name,
                        'geometry', ST_AsGeoJSON(AreaOfInterest.geometry)
                    ).label("area_of_interest")
                )
                .join(AreaOfInterest)
                .where(Project.id == project_id)
            )

            stmt = await session.execute(results)
            result = stmt.fetchone()

            if not result:
                raise NoResultFound()

            project, area_of_interest = result
            resp = ProjectListResponse.model_validate(project, from_attributes=True)

            return {
                **resp.model_dump(),
                "area_of_interest":  {**area_of_interest, "geometry": json.loads(area_of_interest["geometry"])},
            }


project_service = ProjectService(project_repository=projects_repository)
