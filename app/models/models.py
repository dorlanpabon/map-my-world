from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class Location(Base):
    """
    Model representing a geographical location.

    Attributes:
        id (int): The unique identifier of the location.
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        created_at (datetime): The timestamp when the location was created.
    """
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Category(Base):
    """
    Model representing a category.

    Attributes:
        id (int): The unique identifier of the category.
        name (str): The name of the category.
        created_at (datetime): The timestamp when the category was created.
    """
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class LocationCategoryReviewed(Base):
    """
    Model representing the reviewed relationship between a location and a category.

    Attributes:
        id (int): The unique identifier of the reviewed relationship.
        location_id (int): The ID of the related location.
        category_id (int): The ID of the related category.
        last_reviewed (datetime): The timestamp when the relationship was last reviewed.
        location (Location): The related location object.
        category (Category): The related category object.
    """
    __tablename__ = "location_category_reviewed"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    last_reviewed = Column(DateTime, default=None)

    location = relationship("Location")
    category = relationship("Category")
