import enum

from src.db import db
from src.models.model_associations import key_room


class RoomType(enum.Enum):
    Guest = 1
    Staff = 2


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=False, index=True)
    type = db.Column(db.Enum(RoomType), nullable=False, unique=False)
    floor = db.Column(db.Integer, nullable=False, unique=False)
    keys = db.relationship('Key', secondary=key_room, lazy='selectin', back_populates='rooms')
    dead = db.Column(db.Boolean, default=False)

    def __init__(self, name, type, floor, **kwargs):
        if not name:
            raise ValueError("Name cannot be empty")
        if floor < 0:
            raise ValueError("Floor must be a positive number")
        if type not in RoomType:
            raise ValueError("Invalid room type")
        super(Room, self).__init__(name=name, type=type, floor=floor, **kwargs)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.name,
            'floor': self.floor,
            'dead': self.dead,
            'keys': [key.id for key in self.keys]
        }

    def __repr__(self):
        return f"<Room('{self.name}', '{self.type.name}', floor={self.floor})>"
