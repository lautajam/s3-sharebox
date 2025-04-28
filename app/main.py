from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.file_routes import router as file_routes
from routes.roles_routes import router as roles_router

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Gestor S3 API funcionando"}

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(file_routes, prefix="/files", tags=["files"])
app.include_router(roles_router, prefix="/roles", tags=["roles"])
