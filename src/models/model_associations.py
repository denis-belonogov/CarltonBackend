from src.db import db

key_room = db.Table('key_room',
                    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'), primary_key=True),
                    db.Column('key_id', db.Integer, db.ForeignKey('keys.id'), primary_key=True)
                    )
