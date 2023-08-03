from peewee import *

forum_db = SqliteDatabase("forum.db")

class BaseModel(Model):
    class Meta:
        database = forum_db

class UserDB(BaseModel):
    id = AutoField()
    name = CharField(unique = True)

class ThreadDB(BaseModel):
    id = AutoField()
    title = CharField()
    user_id = ForeignKeyField(UserDB, backref = "threads")

class PostDB(BaseModel):
    id = AutoField()
    message = TextField()
    user_id = ForeignKeyField(UserDB, backref = "posts")
    thread_id = ForeignKeyField(ThreadDB, backref = "posts")

if __name__ == "__main__":
    foundPost = PostDB.select().where(PostDB.id == 1).get()
    print({"id" : foundPost.id, "message" : foundPost.message, "user_id" : foundPost.user_id.id})