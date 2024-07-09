from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import categories as crud_categories
from app.schemas import schemas
from app.config.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new category.

    This endpoint creates a new category with the provided data.

    Parameters:
    - **category** (schemas.CategoryCreate): The category data to create, including the name.

    Returns:
    - **schemas.Category**: The created category data including id, name, and created_at timestamp.

    Raises:
    - **HTTPException**: If an unexpected error occurs.
    """
    try:
        created_category = await crud_categories.create_category(db=db, category=category)
        return created_category
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.get("/", response_model=list[schemas.Category])
async def read_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of categories.

    This endpoint returns a list of categories from the database, allowing for pagination.

    Parameters:
    - **skip** (int, optional): The number of categories to skip. Defaults to 0.
    - **limit** (int, optional): The maximum number of categories to return. Defaults to 100.

    Returns:
    - **List[schemas.Category]**: A list of categories.

    Raises:
    - **HTTPException**: If an unexpected error occurs.
    """
    try:
        categories = await crud_categories.get_categories(db=db, skip=skip, limit=limit)
        return categories
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.get("/{category_id}", response_model=schemas.Category)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a category by ID.

    This endpoint retrieves a specific category by its ID.

    Parameters:
    - **category_id** (int): The ID of the category to retrieve.

    Returns:
    - **schemas.Category**: The category data including id, name, and created_at timestamp.

    Raises:
    - **HTTPException**: If the category with the given ID is not found.
    """
    try:
        db_category = await crud_categories.get_category(db=db, category_id=category_id)
        if db_category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return db_category
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.delete("/{category_id}", response_model=schemas.Category)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a category by ID.

    This endpoint deletes a specific category by its ID.

    Parameters:
    - **category_id** (int): The ID of the category to delete.

    Returns:
    - **schemas.Category**: The deleted category data including id, name, and created_at timestamp.

    Raises:
    - **HTTPException**: If the category with the given ID is not found.
    """
    try:
        db_category = await crud_categories.delete_category(db=db, category_id=category_id)
        if db_category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return db_category
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
