from app.database.db_config import Base
from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DateTime, Float, Boolean,
                        UniqueConstraint, Enum as SQLEnum)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.enums import FuelType, IncidentType, DTCCodeSeverity
import datetime


class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(),
                        nullable=False)


class Rental(Base, TimestampMixin):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    workers = relationship('User', back_populates='rental')
    cars = relationship('Car', back_populates='rental')


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    rental_id = Column(Integer, ForeignKey('rentals.id'))
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    rental = relationship('Rental', back_populates='workers')


class Car(Base, TimestampMixin):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    vin = Column(String, unique=True)
    rental_id = Column(Integer, ForeignKey('rentals.id'))
    fuel_type = Column(SQLEnum(FuelType), nullable=False)

    rental = relationship('Rental', back_populates='cars')
    incidents = relationship('Incident', back_populates='car')


class Incident(Base, TimestampMixin):
    __tablename__ = 'incidents'

    id = Column(Integer, primary_key=True)
    type = Column(SQLEnum(IncidentType), nullable=False)
    description = Column(String)
    time = Column(DateTime, nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id'))
    latitude = Column(Float)
    longitude = Column(Float)

    car = relationship('Car', back_populates='incidents')


class DTCCode(Base, TimestampMixin):
    __tablename__ = 'dtc_codes'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    car_type = Column(String)
    car_brand = Column(String)
    fuel_type = Column(SQLEnum(FuelType))
    severity = Column(SQLEnum(DTCCodeSeverity), nullable=False)
    manager_explanation = Column(String, nullable=False)
    action_required = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint('code', 'car_type', 'car_brand',
                         'fuel_type', name='uq_dtc_profile'),
    )
