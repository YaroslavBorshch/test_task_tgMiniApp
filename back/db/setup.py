from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
# from back.models import User
from starlette.config import Config

config = Config(".env")
async def init_db(app):

    await Tortoise.init(
        db_url=config("WEBAPP_PRETTY_LINK"),
        # db_url="sqlite://db.sqlite3",
        modules={"models": ["db.models"]}
    )
    register_tortoise(
        app,
        db_url=config("WEBAPP_PRETTY_LINK"),
        # db_url="sqlite://db.sqlite3",
        modules={"models": ["db.models"]},
        generate_schemas=True,
        add_exception_handlers=True
    )

