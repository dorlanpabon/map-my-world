from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import recommendations as crud_recommendations
from app.schemas import schemas
from app.config.database import get_db
from typing import List

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/fresh/", response_model=List[schemas.LocationCategoryReviewed])
async def get_fresh_recommendations(db: AsyncSession = Depends(get_db)):
    """
    Get fresh recommendations.

    This endpoint returns a list of 10 location-category combinations that have not been reviewed in the last 30 days,
    prioritizing those that have never been reviewed.

    Returns:
    - **List[schemas.LocationCategoryReviewed]**: A list of recommended location-category relationships.

    Raises:
    - **HTTPException**: If an unexpected error occurs.
    """
    try:
        return await crud_recommendations.get_fresh_recommendations(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.get("/never-reviewed/", response_model=List[schemas.LocationCategoryReviewed])
async def get_never_reviewed_recommendations(db: AsyncSession = Depends(get_db)):
    """
    Get never reviewed recommendations.

    This endpoint returns a list of recommendations that have never been reviewed.

    Returns:
        List[schemas.LocationCategoryReviewed]: A list of never reviewed recommendations
    """
    try:
        return await crud_recommendations.get_never_reviewed_recommendations(db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.post("/", response_model=schemas.LocationCategoryReviewed)
async def create_relation(review: schemas.LocationCategoryReviewedCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new relation.

    This endpoint creates a new relation with the provided data.

    Args:
        relation (schemas.LocationCategoryReviewedCreate): The relation data to create, including location_id and category_id.

    Returns:
        schemas.LocationCategoryReviewed: The created relation data including id, location_id, category_id, and last_reviewed timestamp.
    """
    try:
        return await crud_recommendations.create_relation(db=db, location_id=review.location_id, category_id=review.category_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
    
@router.post("/{review_id}/review", response_model=schemas.LocationCategoryReviewed)
async def create_review(review_id: int, db: AsyncSession = Depends(get_db)):
    """
    Create a new review.

    This endpoint creates a new review for a given location and category.

    Args:
        review_id (int): The ID of the review to create.

    Returns:
        schemas.LocationCategoryReviewed: The created review data including id, location_id, category_id, and last_reviewed timestamp.

    Raises:
        HTTPException: If the review with the given ID is not found.
    """
    try:
        return await crud_recommendations.create_review(db=db, review_id=review_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
    
@router.post("/with-review/", response_model=schemas.LocationCategoryReviewed)
async def create_relation_with_review(review: schemas.LocationCategoryReviewedCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new relation with a review.

    This endpoint creates a new relation with a review for a given location and category.

    Args:
        relation (schemas.LocationCategoryReviewedCreate): The relation data to create, including location_id and category_id.

    Returns:
        schemas.LocationCategoryReviewed: The created relation data including id, location_id, category_id, and last_reviewed timestamp.
    """
    try:
        return await crud_recommendations.create_relation_with_review(db=db, location_id=review.location_id, category_id=review.category_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.get("/{review_id}", response_model=schemas.LocationCategoryReviewed)
async def get_review(review_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a review by ID.

    This endpoint retrieves a specific review by its ID.

    Args:
        review_id (int): The ID of the review to retrieve.

    Returns:
        schemas.LocationCategoryReviewed: The review data including id, location_id, category_id, and last_reviewed timestamp.

    Raises:
        HTTPException: If the review with the given ID is not found.
    """
    try:
        review = await crud_recommendations.get_review(db=db, review_id=review_id)
        if review is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return review
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.delete("/{review_id}", response_model=schemas.LocationCategoryReviewed)
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a review by ID.

    This endpoint deletes a specific review by its ID.

    Args:
        review_id (int): The ID of the review to delete.

    Returns:
        schemas.LocationCategoryReviewed: The deleted review data including id, location_id, category_id, and last_reviewed timestamp.

    Raises:
        HTTPException: If the review with the given ID is not found.
    """
    try:
        review = await crud_recommendations.delete_review(db=db, review_id=review_id)
        if review is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return review
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")