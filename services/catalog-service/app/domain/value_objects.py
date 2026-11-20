from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "RUB"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")