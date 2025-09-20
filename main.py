from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from api.routers import user, cost, salary
import os

app = FastAPI()


app.include_router(user.router)
app.include_router(cost.router)
app.include_router(salary.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/{full_path:path}")
def serve_spa(full_path: str):
    print(f"hello {full_path}")
    if full_path.startswith("api") or full_path.startswith("static"):
        print(full_path)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return FileResponse(os.path.join("static", "main.html"))
