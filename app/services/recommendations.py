from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.models import models
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

async def get_fresh_recommendations(db: AsyncSession):
    """
    Fetches 10 recommendations of location-category combinations that have not been reviewed in the last 30 days,
    prioritizing those that never have been reviewed.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[models.LocationCategoryReviewed]: A list of recommended location-category relationships.
    """
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    query = (
        select(models.LocationCategoryReviewed)
        .options(joinedload(models.LocationCategoryReviewed.location), joinedload(models.LocationCategoryReviewed.category))
        .filter(
            (models.LocationCategoryReviewed.last_reviewed.is_(None)) | 
            (models.LocationCategoryReviewed.last_reviewed < thirty_days_ago)
        )
        .order_by(models.LocationCategoryReviewed.last_reviewed.desc())
        .limit(10)
    )
    
    result = await db.execute(query)
    recommendations = result.scalars().all()
    
    return recommendations

async def get_never_reviewed_recommendations(db: AsyncSession):
    """
    Fetches recommendations that have never been reviewed.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[models.LocationCategoryReviewed]: A list of reviewed location-category relationships
        that have never been reviewed.
    """
    result = await db.execute(select(models.LocationCategoryReviewed)
                              .filter(models.LocationCategoryReviewed.last_reviewed.is_(None))
                              .limit(10))
    return result.scalars().all()

async def create_relation(db: AsyncSession, location_id: int, category_id: int):
    """
    Creates a new relation for a given location and category.

    Args:
        db (AsyncSession): The database session.
        location_id (int): The ID of the location.
        category_id (int): The ID of the category.

    Returns:
        models.LocationCategoryReviewed: The newly created relation object.
    """
    relation = models.LocationCategoryReviewed(location_id=location_id, category_id=category_id, last_reviewed=None)
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return relation

async def create_review(db: AsyncSession, review_id: int):
    """
    Creates a new review for a given location and category.

    Args:
        db (AsyncSession): The database session.
        review_id (int): The ID of the review to create.

    Returns:
        models.LocationCategoryReviewed: The updated review object.
    """
    relation = await get_review(db, review_id)
    if not relation:
        return None
    relation.last_reviewed = datetime.utcnow()
    await db.commit()
    await db.refresh(relation)
    return relation

async def create_relation_with_review(db: AsyncSession, location_id: int, category_id: int):
    """
    Creates a new relation for a given location and category, and reviews it.

    Args:
        db (AsyncSession): The database session.
        location_id (int): The ID of the location.
        category_id (int): The ID of the category.
        
    Returns:
        models.LocationCategoryReviewed: The newly created relation object.
    """
    relation = await create_relation(db, location_id, category_id)
    if not relation:
        return None
    return await create_review(db, relation.id)

async def get_review(db: AsyncSession, review_id: int):
    """
    Fetches a review by its ID.

    Args:
        db (AsyncSession): The database session.
        review_id (int): The ID of the review to fetch.

    Returns:
        models.LocationCategoryReviewed: The review object if found, otherwise None.
    """
    result = await db.execute(select(models.LocationCategoryReviewed)
                              .options(selectinload(models.LocationCategoryReviewed.location),
                                       selectinload(models.LocationCategoryReviewed.category))
                              .filter(models.LocationCategoryReviewed.id == review_id))
    return result.scalars().first()

async def delete_review(db: AsyncSession, review_id: int):
    """
    Deletes a review by its ID.

    Args:
        db (AsyncSession): The database session.
        review_id (int): The ID of the review to delete.

    Returns:
        models.LocationCategoryReviewed: The deleted review object if found and deleted, otherwise None.
    """
    review = await get_review(db, review_id)
    if not review:
        return None
    await db.delete(review)
    await db.commit()
    return review
