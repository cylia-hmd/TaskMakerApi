# Import du framework
from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

#Routers
import routers.router_tasks, routers.router_users
# Initialisation de l'API
app = FastAPI(
    title="Tasks Maker",
    description=api_description,
    openapi_tags= tags_metadata
)

# Routers
app.include_router(routers.router_users.router)
app.include_router(routers.router_tasks.router)
