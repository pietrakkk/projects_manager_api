# Project Manager API





### Add database migration:

*docker exec -it projects_manager_api alembic revision --autogenerate -m "<message content>"*


### Run database migration

*docker exec -it projects_manager_api alembic upgrade head*