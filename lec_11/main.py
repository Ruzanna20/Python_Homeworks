import requests

def get():
    url="https://jsonplaceholder.typicode.com/posts"
    response=requests.get(url)
    if response.status_code==200:
        posts=response.json()
        filtered=[i for i in posts if len(i['title'].split())<=6 and len(i['body'].split('\n')) <= 3
            ]
        return filtered
    else:
        print("Failed:")
        return []
print(get())

def create():
    url="https://jsonplaceholder.typicode.com/posts"
    new_post={
        "title":"Ruzanna",
        "body":"I am student in NPUA:",
        "userId":1}

    response=requests.post(url,json=new_post)
    if response.status_code==201:
        created_post=response.json()
        print(created_post)
    else:
        print("Failed:")
create()

def update(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    updated_post={
        "title":"Update title",
        "body":"Update body"
        }

    response=requests.put(url,json=updated_post)
    if response.status_code==200:
        print(response.json())
    else:
        print("Failed:")
update(100)

def delete(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response=requests.delete(url)
    if response.status_code==200:
        print(f"Post {post_id} Id is deleted:")
    else:
        print("Failed:")
delete(101)

