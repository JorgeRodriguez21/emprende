import enum


class PurchaseStatus(enum.Enum):
    ACTIVE = 'activo'
    SOLD = 'vendido'
    CONFIRMED = 'confirmado'
    CANCELLED = 'cancelado'