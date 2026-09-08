import enum


class FuelType(enum.Enum):
    PETROL = 'petrol'
    DIESEL = 'diesel'
    EV = 'ev'
    HYBRID = 'hybrid'


class IncidentType(enum.Enum):
    COLD_ENGINE = 1
    REDLINING = 2
    PEELING_OUT = 3


class CarType(enum.Enum):
    pass


class DTCCodeSeverity(str, enum.Enum):
    UNKNOWN = 'UNKNOWN'
    CRITICAL = 'CRITICAL'
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
