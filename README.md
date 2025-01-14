# Project Manager API

### Run project:

1. Create .env file (you can copy .env.example -> .env for dev usage)
2. Run command:
   *docker-compose up*

3. Add database tables:
   *docker exec -it projects_manager_api alembic upgrade head*

## Useful commands:

### Add database migration:

*docker exec -it projects_manager_api alembic revision --autogenerate -m "<message content>"*

### Run database migration

*docker exec -it projects_manager_api alembic upgrade head*