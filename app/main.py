from fastapi import FastAPI
from routes.user_routes import router as user_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Gestor S3 API funcionando"}

app.include_router(user_router)
