import json
from json import JSONDecodeError

from endpoints.projects.dependencies import get_form_payload
from endpoints.projects.repository import projects_repository
from endpoints.projects.schema import GeoJsonfileType
from endpoints.projects.schema import ProjectCreate
from endpoints.projects.schema import ProjectResponse
from endpoints.projects.service import project_service
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi import status
from fastapi.params import Depends, File
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

router = APIRouter(
    prefix='/projects',
    tags=['Projects'],
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'Resource not found'}
    },
)


@router.get('/', response_model=list[ProjectResponse])
async def get_projects():
    return await projects_repository.list()


@router.post('/', response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate = Depends(get_form_payload),
    file: UploadFile = File(...),
):
    try:
        geojson_data = await file.read()
        geojson_content = json.loads(geojson_data.decode('utf-8'))
    except (JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid file format. The file is not a valid JSON.',
        )

    if geojson_content.get('type') != GeoJsonfileType.feature.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid GeoJSON format')

    if not geojson_content.get('geometry', []):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No valid geometry found')

    return await project_service.create_project(payload=payload, file_content=geojson_content, file_name=file.filename)


@router.get('/{project_id}')
async def get_project(project_id: str):
    try:
        return await project_service.get_project(project_id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')
    except SQLAlchemyError:
        # TODO: log exc
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Cannot download project')
