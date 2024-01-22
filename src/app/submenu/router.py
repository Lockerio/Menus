from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.db import get_db
from app.database.service.menu_service import MenuService
from app.database.service.submenu_service import SubmenuService
from app.submenu.schemas import SubmenuCreateUpdate


submenu_router = APIRouter(prefix="/api/v1")


@submenu_router.post("/menus/{target_menu_id}/submenus/")
def create_submenu(
        submenu_data: SubmenuCreateUpdate,
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    submenu_service = SubmenuService(db)

    try:
        submenu = submenu_service.create(submenu_data.title, submenu_data.description, target_menu_id)
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Invalid menu id")
    except DataError:
        raise HTTPException(status_code=500, detail="Wrong type of id")

    return JSONResponse({
        "id": str(submenu.id),
        "title": submenu.title,
        "description": submenu.description,
        "menu_id": str(submenu.menu_id),
    }, status_code=201)


@submenu_router.get("/menus/{target_menu_id}/submenus/")
def read_submenus(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    submenu_service = SubmenuService(db)
    submenus = submenu_service.read_by_menu_id(target_menu_id)

    response = [{
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "menu_id": str(submenu.menu_id)
        }
        for submenu in submenus
    ]

    return JSONResponse(response)


@submenu_router.get("/menus/{target_menu_id}/submenus/{target_submenu_id}")
def read_submenu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        db: Session = Depends(get_db)
):
    submenu_service = SubmenuService(db)
    submenus = submenu_service.read_by_menu_id(target_menu_id)

    try:
        submenu = submenu_service.read(target_submenu_id)

    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    if submenu in submenus:
        return JSONResponse({
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "menu_id": str(submenu.menu_id)
        })

    raise HTTPException(status_code=404, detail="submenu not found")


@submenu_router.patch("/menus/{target_menu_id}/submenus/{target_submenu_id}")
def update_submenu(
        menu_data: SubmenuCreateUpdate,
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    submenu_service = SubmenuService(db)
    submenus = submenu_service.read_by_menu_id(target_menu_id)

    try:
        submenu = submenu_service.read(target_submenu_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    if submenu in submenus:
        submenu = submenu_service.update(menu_data.title, menu_data.description, target_submenu_id)

        return JSONResponse({
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "menu_id": str(submenu.menu_id)
        })

    raise HTTPException(status_code=404, detail="submenu not found")


@submenu_router.delete("/menus/{target_menu_id}/submenus/{target_submenu_id}")
def delete_submenu(
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    submenu_service = SubmenuService(db)
    submenus = submenu_service.read_by_menu_id(target_menu_id)

    try:
        submenu = submenu_service.read(target_submenu_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    if submenu in submenus:
        try:
            submenu_service.delete(submenu.id)
        except AttributeError:
            raise HTTPException(status_code=500, detail="Something went wrong")

        return JSONResponse(None)
    raise HTTPException(status_code=404, detail="submenu not found")