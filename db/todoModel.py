import orm
from db.init_db import database, metadata


class TodoList(orm.Model):

    __tablename__ = "todo"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    title = orm.String(max_length=30, allow_null=False)
    status = orm.Boolean(default=False)
    info = orm.Text()
    created_at = orm.DateTime()
    updated_at = orm.DateTime()
    deleted_at = orm.DateTime()
