# forum_client.py - capage
# Built to meet ForumAPISpec.md

# Limitations:
# - Does not handle errors at all
# - Currently doesn't allow the creation of new posts
# - Horrible mess in places
# - Fetching is handled asynchronously so loading a thread is slow!

from typing import Dict, List

import requests


class ForumAPIService:
    def __init__(self, url):
        self.url = url

    def get_user(self, user_id: int) -> Dict:
        r = requests.get("{}/users/{}".format(self.url, user_id))
        if r.status_code == 200:
            return r.json()

    def get_users(self) -> List[Dict]:
        r = requests.get("{}/users".format(self.url))
        if r.status_code == 200:
            return r.json()

    def make_user(self, username: str) -> int:
        r = requests.post("{}/users".format(self.url), json={"name": username})
        if r.status_code == 200 or r.status_code == 201:
            # This should be 201, but 200 is accepted just in case
            return int(r.content)

    def get_thread(self, thread_id: int) -> Dict:
        r = requests.get("{}/threads/{}".format(self.url, thread_id))
        if r.status_code == 200:
            return r.json()

    def get_threads(self) -> List[Dict]:
        r = requests.get("{}/threads".format(self.url))
        if r.status_code == 200:
            return r.json()

    def make_thread(self, user_id: int, title: str) -> int:
        r = requests.post("{}/threads".format(self.url), json={"title": title, "user_id": user_id})
        if r.status_code == 200 or r.status_code == 201:
            # This should be 201, but 200 is accepted just in case
            return int(r.content)

    def get_post(self, thread_id: int, post_id: int) -> Dict:
        r = requests.get("{}/threads/{}/posts/{}".format(self.url, thread_id, post_id))
        if r.status_code == 200:
            return r.json()

    def get_posts(self, thread_id: int) -> List[Dict]:
        r = requests.get("{}/threads/{}/posts".format(self.url, thread_id))
        if r.status_code == 200:
            return r.json()

    def make_post(self, thread_id: int, user_id: int, message: str) -> int:
        r = requests.post("{}/threads/{}/posts".format(self.url, thread_id),
                          json={"user_id": user_id, "message": message})


def main_menu():
    currentuser = None
    command = None
    apiservice = ForumAPIService("http://localhost:5000")
    while command != 99:
        if currentuser is not None:
            user = apiservice.get_user(currentuser)
            print("Currently logged in user: {}".format(user.get("name")))
        else:
            print("Not currently logged in.")
        print("1. Select user. \n2. Create user. \n3. Show All Threads \n4. Show Thread \n5. Post New Thread")
        print("Command: ", end="")
        command = int(input())
        if command == 1:
            currentuser = select_user(apiservice, currentuser)
        elif command == 2:
            currentuser = create_user(apiservice, currentuser)
        elif command == 3:
            show_all_threads(apiservice)
        elif command == 4:
            show_thread(apiservice)
        elif command == 5:
            post_new_thread(apiservice, currentuser)
        input()


def select_user(apiservice: ForumAPIService, currentuser: int) -> int:
    users = apiservice.get_users()
    print("User list: ")
    for u in users:
        print("{} - {}".format(u.get("id"), u.get("name")))

    print("Please select a user id: ", end="")
    new_userid = int(input())
    return new_userid


def create_user(apiservice: ForumAPIService, currentuser: int) -> int:
    print("Please insert your new username: ", end="")
    new_username = input()

    new_userid = apiservice.make_user(new_username)
    return new_userid


def show_all_threads(apiservice: ForumAPIService) -> None:
    threads = apiservice.get_threads()
    for t in threads:
        print("Thread {} - Title: {} - Posts: {}".format(t.get("id"), t.get("title"), len(t.get("posts", []))))


def show_thread(apiservice: ForumAPIService) -> None:
    print("Please insert a thread id to read: ", end="")
    thread_id = int(input())
    thread = apiservice.get_thread(thread_id)
    thread_user = apiservice.get_user(thread.get("user_id"))
    print("{} by {}".format(thread.get("title"), thread_user.get("name")))
    for p in thread.get("posts"):
        post = apiservice.get_post(thread.get("id"), p)
        post_user = apiservice.get_user(post.get("user_id"))
        print("Post {} by {}".format(post.get("id"), post_user.get("name")))
        print("{}\n".format(post.get("message")))


def post_new_thread(apiservice: ForumAPIService, currentuser : int) -> None:
    print("Please insert a new thread title: ", end="")
    thread_title = input()
    new_threadid = apiservice.make_thread(currentuser,thread_title)
    print("Thread created with id {}".format(new_threadid))




if __name__ == "__main__":
    main_menu()
