import uvicorn
from fastapi import FastAPI

from app.dish.router import dish_router
from app.menu.router import menu_router
from app.submenu.router import submenu_router

app = FastAPI(prefix="/api/v1", title="Menus Service", debug=True)

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
