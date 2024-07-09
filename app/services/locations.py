from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import models
from app.schemas import schemas

async def get_location(db: AsyncSession, location_id: int):
    """
    Fetches a location by its ID.

    Args:
        db (AsyncSession): The database session.
        location_id (int): The ID of the location to fetch.

    Returns:
        models.Location: The location object if found, otherwise None.
    """
    result = await db.execute(select(models.Location).filter(models.Location.id == location_id))
    return result.scalars().first()
    
async def create_location(db: AsyncSession, location: schemas.LocationCreate):
    """
    Creates a new location.

    Args:
        db (AsyncSession): The database session.
        location (schemas.LocationCreate): The location data to create.

    Returns:
        models.Location: The newly created location object.
    """
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    await db.commit()
    await db.refresh(db_location)
    return db_location

async def get_locations(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Fetches multiple locations with pagination.

    Args:
        db (AsyncSession): The database session.
        skip (int): The number of records to skip for pagination. Default is 0.
        limit (int): The maximum number of records to return. Default is 100.

    Returns:
        List[models.Location]: A list of location objects.
    """
    result = await db.execute(select(models.Location).offset(skip).limit(limit))
    return result.scalars().all()

async def delete_location(db: AsyncSession, location_id: int):
    """
    Deletes a location by its ID.

    Args:
        db (AsyncSession): The database session.
        location_id (int): The ID of the location to delete.

    Returns:
        models.Location: The deleted location object if found and deleted, otherwise None.
    """
    db_location = await get_location(db, location_id)
    if not db_location:
        return None
    await db.delete(db_location)
    await db.commit()
    return db_location

async def update_location(db: AsyncSession, location_id: int, location: schemas.LocationCreate):
    """
    Updates an existing location by its ID.

    Args:
        db (AsyncSession): The database session.
        location_id (int): The ID of the location to update.
        location (schemas.LocationCreate): The new location data.

    Returns:
        models.Location: The updated location object if found and updated, otherwise None.
    """
    db_location = await get_location(db, location_id)
    if not db_location:
        return None
    db_location.latitude = location.latitude
    db_location.longitude = location.longitude
    await db.commit()
    await db.refresh(db_location)
    return db_location
