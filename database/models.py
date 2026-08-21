from database.db_config import Base
from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DateTime, Float, Enum as SQLEnum)
from sqlalchemy.orm import relationship
from enums import FuelType, IncidentType


class Rental(Base):
    __tablename__ = 'rentals'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    workers = relationship('User', back_populates='rental')
    cars = relationship('Car', back_populates='rental')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    rental_id = Column(Integer, ForeignKey('rentals.id'))
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    rental = relationship('Rental', back_populates='workers')


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    vin = Column(String, unique=True)
    rental_id = Column(Integer, ForeignKey('rentals.id'))
    fuel_type = Column(SQLEnum(FuelType), nullable=False)
    rental = relationship('Rental', back_populates='cars')
    incidents = relationship('Incident', back_populates='car')


class Incident(Base):
    __tablename__ = 'incidents'
    id = Column(Integer, primary_key=True)
    type = Column(SQLEnum(IncidentType), nullable=False)
    description = Column(String)
    time = Column(DateTime, nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id'))
    latitude = Column(Float)
    longitude = Column(Float)

    car = relationship('Car', back_populates='incidents')
