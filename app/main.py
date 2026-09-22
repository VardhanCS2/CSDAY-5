from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

from app.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    ProductCreate,
    ProductUpdate,
    ProductResponse
)

from app.crud import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="FastAPI CRUD API",
    description="User and Product CRUD API using FastAPI, Pydantic, SQLAlchemy and PostgreSQL",
    version="1.0.0"
)


# =========================================================
# USER APIs
# =========================================================


# CREATE USER
@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
async def create_user_api(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_user(
        db,
        user_data
    )


# GET ALL USERS
@app.get(
    "/users",
    response_model=list[UserResponse]
)
async def get_users_api(
    db: AsyncSession = Depends(get_db)
):
    return await get_users(db)


# GET ONE USER
@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
async def get_user_api(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# UPDATE USER
@app.put(
    "/users/{user_id}",
    response_model=UserResponse
)
async def update_user_api(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await update_user(
        db,
        user_id,
        user_data
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# DELETE USER
@app.delete(
    "/users/{user_id}"
)
async def delete_user_api(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await delete_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }


# =========================================================
# PRODUCT APIs
# =========================================================


# CREATE PRODUCT
@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=201
)
async def create_product_api(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check whether the user exists
    user = await get_user(
        db,
        product_data.user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return await create_product(
        db,
        product_data
    )


# GET ALL PRODUCTS
@app.get(
    "/products",
    response_model=list[ProductResponse]
)
async def get_products_api(
    db: AsyncSession = Depends(get_db)
):
    return await get_products(db)


# GET ONE PRODUCT
@app.get(
    "/products/{product_id}",
    response_model=ProductResponse
)
async def get_product_api(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    product = await get_product(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# UPDATE PRODUCT
@app.put(
    "/products/{product_id}",
    response_model=ProductResponse
)
async def update_product_api(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    product = await update_product(
        db,
        product_id,
        product_data
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# DELETE PRODUCT
@app.delete(
    "/products/{product_id}"
)
async def delete_product_api(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    product = await delete_product(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }