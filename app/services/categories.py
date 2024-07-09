from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import models
from app.schemas import schemas

async def get_category(db: AsyncSession, category_id: int):
    """
    Fetches a category by its ID.

    Args:
        db (AsyncSession): The database session.
        category_id (int): The ID of the category to fetch.

    Returns:
        models.Category: The category object if found, otherwise None.
    """
    result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    return result.scalars().first()

async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    """
    Creates a new category.

    Args:
        db (AsyncSession): The database session.
        category (schemas.CategoryCreate): The category data to create.

    Returns:
        models.Category: The newly created category object.
    """
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Fetches multiple categories with pagination.

    Args:
        db (AsyncSession): The database session.
        skip (int): The number of records to skip for pagination. Default is 0.
        limit (int): The maximum number of records to return. Default is 100.

    Returns:
        List[models.Category]: A list of category objects.
    """
    result = await db.execute(select(models.Category).offset(skip).limit(limit))
    return result.scalars().all()

async def delete_category(db: AsyncSession, category_id: int):
    """
    Deletes a category by its ID.

    Args:
        db (AsyncSession): The database session.
        category_id (int): The ID of the category to delete.

    Returns:
        models.Category: The deleted category object if found and deleted, otherwise None.
    """
    db_category = await get_category(db, category_id)
    if not db_category:
        return None
    await db.delete(db_category)
    await db.commit()
    return db_category

async def update_category(db: AsyncSession, category_id: int, category: schemas.CategoryCreate):
    """
    Updates an existing category by its ID.

    Args:
        db (AsyncSession): The database session.
        category_id (int): The ID of the category to update.
        category (schemas.CategoryCreate): The new category data.

    Returns:
        models.Category: The updated category object if found and updated, otherwise None.
    """
    db_category = await get_category(db, category_id)
    if not db_category:
        return None
    db_category.name = category.name
    await db.commit()
    await db.refresh(db_category)
    return db_category
