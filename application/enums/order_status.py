import enum


class OrderStatus(enum.Enum):
    PENDING = 'pendiente'
    CONFIRMED = 'confirmado'