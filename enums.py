import enum


class FuelType(enum.Enum):
    PETROL = 'petrol'
    DIESEL = 'Diesel'
    EV = 'ev'
    HYBRID = 'hybrid'


class IncidentType(enum.Enum):
    COLD_ENGINE = 1
    REDLINING = 2
