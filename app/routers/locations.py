from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import locations as crud_locations
from app.schemas import schemas
from app.config.database import SessionLocal, get_db

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.post("/", response_model=schemas.Location, status_code=status.HTTP_201_CREATED)
async def create_location(location: schemas.LocationCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a location.
    
    This endpoint creates a new location with the provided latitude and longitude.

    Parameters:
    - **location** (schemas.LocationCreate): The location data to create, including latitude and longitude.

    Returns:
    - **schemas.Location**: The created location data including id, latitude, longitude, and created_at timestamp.

    Raises:
    - **HTTPException**: If an unexpected error occurs.
    """
    try:
        return await crud_locations.create_location(db=db, location=location)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.get("/", response_model=list[schemas.Location])
async def read_locations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve locations.

    This endpoint returns a list of locations from the database, allowing for pagination.

    Parameters:
    - **skip** (int, optional): The number of locations to skip. Defaults to 0.
    - **limit** (int, optional): The maximum number of locations to return. Defaults to 100.

    Returns:
    - **List[schemas.Location]**: A list of locations.

    Raises:
    - **HTTPException**: If an unexpected error occurs.
    """
    try:
        return await crud_locations.get_locations(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.get("/{location_id}", response_model=schemas.Location)
async def read_location(location_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a location by ID.

    This endpoint retrieves a specific location by its ID.

    Parameters:
    - **location_id** (int): The ID of the location to retrieve.

    Returns:
    - **schemas.Location**: The location data including id, latitude, longitude, and created_at timestamp.

    Raises:
    - **HTTPException**: If the location with the given ID is not found.
    - **HTTPException**: If an unexpected error occurs.
    """
    try:
        db_location = await crud_locations.get_location(db=db, location_id=location_id)
        if db_location is None:
            raise HTTPException(status_code=404, detail="Location not found")
        return db_location
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.delete("/{location_id}", response_model=schemas.Location)
async def delete_location(location_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a location by ID.

    This endpoint deletes a specific location by its ID.

    Parameters:
    - **location_id** (int): The ID of the location to delete.

    Returns:
    - **schemas.Location**: The deleted location data including id, latitude, longitude, and created_at timestamp.

    Raises:
    - **HTTPException**: If the location with the given ID is not found.
    - **HTTPException**: If an unexpected error occurs.
    """
    try:
        db_location = await crud_locations.delete_location(db=db, location_id=location_id)
        if db_location is None:
            raise HTTPException(status_code=404, detail="Location not found")
        return db_location
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
