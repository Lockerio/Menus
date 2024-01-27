from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.database.db import get_db
from app.database.service.menu_service import MenuService
from app.database.service.submenu_service import SubmenuService
from app.submenu.schemas import SubmenuCreateUpdate


submenu_router = APIRouter(prefix="/api/v1")


@submenu_router.post("/menus/{target_menu_id}/submenus/")
async def create_submenu(
        submenu_data: SubmenuCreateUpdate,
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        menu_service = MenuService(db)
        submenu_service = SubmenuService(db)

        try:
            menu = await menu_service.read(target_menu_id)
            if menu:
                submenu = await submenu_service.create(submenu_data.title, submenu_data.description, target_menu_id)
            else:
                raise HTTPException(status_code=500, detail=f"There is no menu with id {target_menu_id}")

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
async def read_submenus(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        submenu_service = SubmenuService(db)
        submenus = await submenu_service.read_by_menu_id(target_menu_id)

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
async def read_submenu(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        submenu_service = SubmenuService(db)
        submenus = await submenu_service.read_by_menu_id(target_menu_id)

        try:
            submenu = await submenu_service.read(target_submenu_id)
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    if submenu in submenus:
        return JSONResponse({
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "menu_id": str(submenu.menu_id),
            "dishes_count": len(submenu.dishes)
        })

    raise HTTPException(status_code=404, detail="submenu not found")


@submenu_router.patch("/menus/{target_menu_id}/submenus/{target_submenu_id}")
async def update_submenu(
        menu_data: SubmenuCreateUpdate,
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        submenu_service = SubmenuService(db)
        submenus = await submenu_service.read_by_menu_id(target_menu_id)

        try:
            submenu = await submenu_service.read(target_submenu_id)
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

        if submenu in submenus:
            submenu = await submenu_service.update(menu_data.title, menu_data.description, target_submenu_id)

            return JSONResponse({
                "id": str(submenu.id),
                "title": submenu.title,
                "description": submenu.description,
                "menu_id": str(submenu.menu_id)
            })

        raise HTTPException(status_code=404, detail="submenu not found")


@submenu_router.delete("/menus/{target_menu_id}/submenus/{target_submenu_id}")
async def delete_submenu(
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        submenu_service = SubmenuService(db)
        submenus = await submenu_service.read_by_menu_id(target_menu_id)

        try:
            submenu = await submenu_service.read(target_submenu_id)
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

        if submenu in submenus:
            try:
                await submenu_service.delete(submenu)
            except AttributeError:
                raise HTTPException(status_code=500, detail="Something went wrong")

            return JSONResponse(None)
        raise HTTPException(status_code=404, detail="submenu not found")
