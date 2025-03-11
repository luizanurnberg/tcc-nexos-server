from datetime import datetime


class ClientModel:
    def __init__(
        self,
        id,
        email,
        name,
        weight,
        created_at,
        created_by_id,
    ):
        self.ID = id
        self.EMAIL = email
        self.NAME = name
        self.WEIGHT = weight
        self.CREATED_AT = created_at
        self.CREATED_BY_ID = created_by_id

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("clientId"),
            name=data.get("clientName"),
            weight=data.get("clientWeight"),
            email=data.get("clientEmail"),
            created_at=datetime.utcnow(),
            created_by_id=data.get("user"),
        )

    def to_dict(self):
        return self.__dict__
