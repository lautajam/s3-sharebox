from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Gestor S3 API funcionando"}
