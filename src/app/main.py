import uvicorn
from fastapi import FastAPI

from app.menu.router import menu_router


app = FastAPI(prefix="/api/v1", title="Menus Service", debug=True)

app.include_router(menu_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
