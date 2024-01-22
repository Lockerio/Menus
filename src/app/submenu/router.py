from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.db import get_db
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
        "menu_id": target_menu_id,
        "description": submenu.description
    }, status_code=201)


@submenu_router.get("/menus/")
def read_submenus(
        db: Session = Depends(get_db)
):
    menu_service = SubmenuCreateUpdate(db)
    menus = menu_service.read_all()

    response = [{
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description
        }
        for submenu in menus
    ]

    return JSONResponse(response)


@submenu_router.get("/menus/{target_menu_id}/")
def read_submenu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    menu_service = SubmenuCreateUpdate(db)

    try:
        submenu = menu_service.read(target_menu_id)

    except:
        raise HTTPException(status_code=404, detail="Something went wrong")

    if submenu:
        return JSONResponse({
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description
        })

    raise HTTPException(status_code=404, detail="submenu not found")


@submenu_router.patch("/menus/{target_menu_id}/")
def update_submenu(
        menu_data: SubmenuCreateUpdate,
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    menu_service = SubmenuService(db)

    try:
        submenu = menu_service.update(menu_data.title, menu_data.description, target_menu_id)

    except:
        raise HTTPException(status_code=404, detail="Something went wrong")

    if submenu:
        return JSONResponse({
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description
        })

    raise HTTPException(status_code=404, detail="submenu not found")


@submenu_router.delete("/menus/{target_menu_id}/")
def delete_submenu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: Session = Depends(get_db)
):
    menu_service = SubmenuService(db)

    try:
        menu_service.delete(target_menu_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Something went wrong")

    return JSONResponse(None)
