from fastapi import APIRouter, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.database.db import get_db
from app.database.service.menu_service import MenuService
from app.menu.schemas import MenuCreateUpdate


menu_router = APIRouter(prefix="/api/v1")


@menu_router.post("/menus/")
def create_menu(
        menu_data: MenuCreateUpdate,
        db: Session = Depends(get_db)
):
    menu_service = MenuService(db)
    menu = menu_service.create(menu_data.title, menu_data.description)
    return JSONResponse({
        "id": str(menu.id),
        "title": menu.title,
        "description": menu.description
    }, status_code=201)


@menu_router.get("/menus/")
def read_menus(
        db: Session = Depends(get_db)
):
    menu_service = MenuService(db)
    menus = menu_service.read_all()

    response = [{
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description
        }
        for menu in menus
    ]

    return JSONResponse(response)


@menu_router.get("/menus/{target_menu_id}/")
def read_menu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    menu_service = MenuService(db)

    try:
        menu = menu_service.read(target_menu_id)

    except:
        raise HTTPException(status_code=404, detail="Something went wrong")

    if menu:
        return JSONResponse({
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description
        })

    raise HTTPException(status_code=404, detail="menu not found")


@menu_router.patch("/menus/{target_menu_id}/")
def update_menu(
        menu_data: MenuCreateUpdate,
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    menu_service = MenuService(db)

    try:
        menu = menu_service.update(menu_data.title, menu_data.description, target_menu_id)

    except:
        raise HTTPException(status_code=404, detail="Something went wrong")

    if menu:
        return JSONResponse({
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description
        })

    raise HTTPException(status_code=404, detail="menu not found")


@menu_router.delete("/menus/{target_menu_id}/")
def delete_menu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    menu_service = MenuService(db)

    try:
        menu_service.delete(target_menu_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Something went wrong")

    return JSONResponse(None)
