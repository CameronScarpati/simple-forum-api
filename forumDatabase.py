from peewee import *

forum_db = SqliteDatabase("forum.db")

class BaseModel(Model):
    class Meta:
        database = forum_db

class User(BaseModel):
    id = IntegerField()
    name = CharField()

class Post(BaseModel):
    id = IntegerField()
    message = TextField()
    user_id = ForeignKeyField(User, backref = "id")

class Thread(BaseModel):
    id = IntegerField()
    title = CharField()
    user_id = ForeignKeyField(User, backref = "id")
    posts = ForeignKeyField(Post)

if __name__ == "__main__":
    forum_db.connect()
    forum_db.create_tables([User, Post, Thread])