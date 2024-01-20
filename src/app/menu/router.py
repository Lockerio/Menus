from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.database.db import get_db
from app.database.service.menu_service import MenuService


menu_router = APIRouter()


@menu_router.get("/menus/{target_menu_id}")
def read_menu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    menu_service = MenuService(db)
    menu = menu_service.read(target_menu_id)
    return JSONResponse(content=menu)


@menu_router.patch("/menus/{target_menu_id}")
def read_menu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    menu_service = MenuService(db)
    menu = menu_service.read(target_menu_id)
    return JSONResponse(content=menu)
