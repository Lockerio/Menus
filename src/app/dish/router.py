from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.database.db import get_db
from app.database.service.dish_service import DishService
from app.database.service.submenu_service import SubmenuService
from app.dish.schemas import DishCreateUpdate


dish_router = APIRouter(prefix="/api/v1")


@dish_router.post("/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/")
async def create_dish(
        submenu_data: DishCreateUpdate,
        target_menu_id: str = Path(..., title="Target Menu ID"),
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        submenu_service = SubmenuService(db)
        dish_service = DishService(db)

        try:
            submenus = await submenu_service.read_submenu_ids_by_menu_id(target_menu_id)
            submenu = await submenu_service.read(target_submenu_id)

            if submenu.id in submenus:
                dish = await dish_service.create(
                    submenu_data.title,
                    submenu_data.description,
                    submenu_data.price,
                    target_submenu_id
                )
            else:
                raise HTTPException(status_code=500, detail=f"There is no submenu with id {target_submenu_id}")

        except IntegrityError:
            raise HTTPException(status_code=500, detail="Invalid menu id")
        except DataError:
            raise HTTPException(status_code=500, detail="Wrong type of id")

    return JSONResponse({
        "id": str(dish.id),
        "title": dish.title,
        "description": dish.description,
        "price": dish.price,
        "submenu_id": str(dish.submenu_id),
    }, status_code=201)


@dish_router.get("/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/")
async def read_dishes(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        dish_service = DishService(db)
        dishes = await dish_service.read_by_submenu_id(target_submenu_id)

    response = [{
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": dish.price,
            "submenu_id": str(dish.submenu_id)
        }
        for dish in dishes
    ]

    return JSONResponse(response)


@dish_router.get("/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def read_dish(
        target_menu_id: str = Path(..., title="Target Menu ID"),
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        target_dish_id: str = Path(..., title="Target Dish ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        dish_service = DishService(db)
        dishes = await dish_service.read_by_submenu_id(target_submenu_id)

        try:
            dish = await dish_service.read(target_dish_id)
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    if dish in dishes:
        return JSONResponse({
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": dish.price,
            "submenu_id": str(dish.submenu_id)
        })

    raise HTTPException(status_code=404, detail="dish not found")


@dish_router.patch("/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def update_dish(
        menu_data: DishCreateUpdate,
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        target_dish_id: str = Path(..., title="Target Dish ID"),
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        dish_service = DishService(db)

        try:
            dishes = await dish_service.read_by_submenu_id(target_submenu_id)
            dish = await dish_service.read(target_dish_id)
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

        if dish in dishes:
            dish = await dish_service.update(menu_data.title, menu_data.description, menu_data.price, target_dish_id)

            return JSONResponse({
                "id": str(dish.id),
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
                "submenu_id": str(dish.submenu_id)
            })

        raise HTTPException(status_code=404, detail="dish not found")


@dish_router.delete("/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def delete_dish(
        target_submenu_id: str = Path(..., title="Target Submenu ID"),
        target_dish_id: str = Path(..., title="Target Dish ID"),
        target_menu_id: str = Path(..., title="Target Menu ID"),
        db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        dish_service = DishService(db)

        try:
            dishes = await dish_service.read_by_submenu_id(target_submenu_id)
            dish = await dish_service.read(target_dish_id)
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

        if dish in dishes:
            try:
                await dish_service.delete(dish.id)
            except AttributeError:
                raise HTTPException(status_code=500, detail="Something went wrong")

            return JSONResponse(None)
    raise HTTPException(status_code=404, detail="dish not found")
