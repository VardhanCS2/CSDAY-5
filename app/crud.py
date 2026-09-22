from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Product
from app.schemas import (
    UserCreate,
    UserUpdate,
    ProductCreate,
    ProductUpdate
)


# =========================================================
# USER CRUD
# =========================================================


# CREATE USER
async def create_user(
    db: AsyncSession,
    user_data: UserCreate
):
    user = User(
        name=user_data.name,
        email=user_data.email,
        age=user_data.age
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


# GET ALL USERS
async def get_users(
    db: AsyncSession
):
    result = await db.execute(
        select(User)
    )

    return result.scalars().all()


# GET ONE USER
async def get_user(
    db: AsyncSession,
    user_id: int
):
    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    return result.scalar_one_or_none()


# UPDATE USER
async def update_user(
    db: AsyncSession,
    user_id: int,
    user_data: UserUpdate
):
    user = await get_user(
        db,
        user_id
    )

    if user is None:
        return None

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


# DELETE USER
async def delete_user(
    db: AsyncSession,
    user_id: int
):
    user = await get_user(
        db,
        user_id
    )

    if user is None:
        return None

    await db.delete(user)
    await db.commit()

    return user


# =========================================================
# PRODUCT CRUD
# =========================================================


# CREATE PRODUCT
async def create_product(
    db: AsyncSession,
    product_data: ProductCreate
):
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        user_id=product_data.user_id
    )

    db.add(product)

    await db.commit()
    await db.refresh(product)

    return product


# GET ALL PRODUCTS
async def get_products(
    db: AsyncSession
):
    result = await db.execute(
        select(Product)
    )

    return result.scalars().all()


# GET ONE PRODUCT
async def get_product(
    db: AsyncSession,
    product_id: int
):
    result = await db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    return result.scalar_one_or_none()


# UPDATE PRODUCT
async def update_product(
    db: AsyncSession,
    product_id: int,
    product_data: ProductUpdate
):
    product = await get_product(
        db,
        product_id
    )

    if product is None:
        return None

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product


# DELETE PRODUCT
async def delete_product(
    db: AsyncSession,
    product_id: int
):
    product = await get_product(
        db,
        product_id
    )

    if product is None:
        return None

    await db.delete(product)
    await db.commit()

    return product