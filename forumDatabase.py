from peewee import *

forum_db = SqliteDatabase("forum.db")

class BaseModel(Model):
    class Meta:
        database = forum_db

class UserDB(BaseModel):
    id = AutoField()
    name = CharField(unique = True)

class PostDB(BaseModel):
    id = AutoField()
    message = TextField()
    user_id = ForeignKeyField(UserDB, backref = "users")

class ThreadDB(BaseModel):
    id = AutoField()
    title = CharField()
    user_id = ForeignKeyField(UserDB, backref = "users")
    posts = ForeignKeyField(PostDB)

if __name__ == "__main__":
    pass