from src.db import db
from src.models.model_associations import key_room


class Key(db.Model):
    __tablename__ = 'keys'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(20), nullable=True, unique=False)
    name = db.Column(db.String(20), nullable=True, unique=False, index=True)
    amount = db.Column(db.Integer, nullable=False, unique=False)
    rooms = db.relationship('Room', secondary=key_room, lazy='selectin', back_populates='keys')

    def __init__(self, brand, name, amount, **kwargs):
        if not brand:
            raise ValueError("Brand cannot be empty")
        if not name:
            raise ValueError("Name cannot be empty")
        if amount <= 0:
            raise ValueError("Amount must be a positive number")
        super(Key, self).__init__(brand=brand, name=name, amount=amount, **kwargs)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'amount': self.amount,
            'rooms': [room.id for room in self.rooms]
        }

    def __repr__(self):
        return f"<Key('{self.name}', '{self.brand}', amount={self.amount})>"
