from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class LocationBase(BaseModel):
    """
    Base model for location data.
    
    Attributes:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
    """
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    """
    Model for creating a new location.
    Inherits from LocationBase and adds no additional attributes.
    """
    pass

class Location(LocationBase):
    """
    Model representing a location in the database.
    
    Attributes:
        id (int): The unique identifier of the location.
        created_at (datetime): The timestamp when the location was created.
    """
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    """
    Base model for category data.
    
    Attributes:
        name (str): The name of the category.
    """
    name: str

class CategoryCreate(CategoryBase):
    """
    Model for creating a new category.
    Inherits from CategoryBase and adds no additional attributes.
    """
    pass

class Category(CategoryBase):
    """
    Model representing a category in the database.
    
    Attributes:
        id (int): The unique identifier of the category.
        created_at (datetime): The timestamp when the category was created.
    """
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class LocationCategoryReviewedBase(BaseModel):
    """
    Base model for reviewed location-category relationship.
    
    Attributes:
        location_id (int): The ID of the location.
        category_id (int): The ID of the category.
    """
    location_id: int
    category_id: int

class LocationCategoryReviewedCreate(LocationCategoryReviewedBase):
    """
    Model for creating a new reviewed location-category relationship.
    Inherits from LocationCategoryReviewedBase and adds no additional attributes.
    """
    pass

class LocationCategoryReviewed(LocationCategoryReviewedBase):
    """
    Model representing a reviewed location-category relationship in the database.
    
    Attributes:
        id (int): The unique identifier of the reviewed relationship.
        last_reviewed (datetime): The timestamp when the relationship was last reviewed.
    """
    id: int
    last_reviewed: Optional[datetime] = None

    class Config:
        orm_mode = True
