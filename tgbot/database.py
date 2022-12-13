from tortoise import Tortoise
from tortoise.models import Model
from tortoise import fields
from tgbot import config


class Users(Model):
    user_id = fields.IntField(pk=True)
    status = fields.TextField()
    login = fields.TextField(null=True)
    password = fields.TextField(null=True)
    notification = fields.IntField()

    def __int__(self):
        return self.user_id


async def run_database():
    await Tortoise.init(
        db_url=f'postgres://{config.postgres["user"]}:{config.postgres["password"]}@'
               f'{config.postgres["host"]}:{config.postgres["port"]}/{config.postgres["db"]}',
        modules={'models': ['tgbot.database']}
    )
    await Tortoise.generate_schemas()
