from tortoise import Model, fields
from datetime import date
from typing import Dict, Any


class User(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.CharField(max_length=64, unique=True)
    name = fields.CharField(max_length=255)
    surname = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255)
    birthday = fields.DateField()
    self_link = fields.CharField(max_length=32, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    @property
    def to_json(self) -> Dict[str, Any]:
        """сериалайзер"""
        return {
            "tg_id": self.tg_id,
            "name": self.name,
            "surname": self.surname,
            "username": self.username,
            "birthday": self.birthday.strftime("%Y-%m-%d"),
            "self_link": self.self_link,
            "is_serialized": True
        }

    class Meta:
        table = "users"

