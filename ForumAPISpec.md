# Users
## `POST /users`

Request Body: `{"name" : String}`

Response: user id (Integer)

Errors: 500 (if username is already taken)

## `GET /users/[id]`

NO REQUEST BODY

Response: `{"id" : Integer, "name" : String}`

Errors: 404 (if user id does not exist)

## `GET /users`

NO REQUEST BODY

Response: `[{"id" : Integer, "name" : String}, ...]`

---
# Threads
## `POST /threads`

Request Body: `{"user_id" : Integer, "title" : String}`

Response: thread id (Integer)

## `GET /threads/[id]`

NO REQUEST BODY

Response: `{"id" : Integer, "title" : String, "posts" : [Integer]}`

Errors: 404 (if thread id does not exist)

Note: posts contains a list of post ids

## `GET /threads`

NO REQUEST BODY

Response: `[{"id" : Integer, "title" : String, "posts": [Integer]}, ... ]`

---

## `POST /threads/[thread_id]/posts`

Request Body: `{"message" : String, "user" : Integer}`

Response: post id (Integer)

Errors: 404 (if thread id is not found), 500 (if user does not exist)

## `GET /threads/[thread_id]/posts`

NO REQUEST BODY

Response: `[{"id" : Integer, "message" : String, "user_id" : Integer}, ...]`

Errors: 404 (if thread id is not found)

## `GET /threads/[thread_id]/posts/[post_id]`

NO REQUEST BODY

Response: `{"id" : Integer, "message" : String, "user_id" : Integer}`

Errors: 404 (if thread id is not found), 404 (if post id is not found), 500 (if post is not in that thread)