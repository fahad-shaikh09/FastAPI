from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
          return post

def find_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

my_posts = [
    {
    "title": "title of post 1",
    "content" : "content of post 1",
    "id": 1
    },
    {
    "title": "title of post 2",
     "content" : "content of post 2",
     "id": 2
     }
]

@app.get("/")
async def get_user():
    return {"message": "hi World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# @app.post("/createpost")
# def createpost(payLoad : dict = Body(...)):
#     print(payLoad)
#     return {"new post": f"Fruit {payLoad['fruit']} Season {payLoad['season']}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    print(post)
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": my_posts}


@app.get ("/posts/latest")
def get_latest_post():
    recent_post= my_posts[-1]
    print(recent_post)
    return {"Recent post" : recent_post}


@app.get("/posts/{id}")
def get_single_post(id: int):
    print(id)
    searched_post = find_post(id)
    if not searched_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doesnt exist") 
    return {"Your searched post is ": searched_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    print("Post with ID to be deleted : " + str(id))
    index = find_index(id)
    print("Post exists at index " +  str(index))
    my_posts.pop(index)
    return {status.HTTP_204_NO_CONTENT}  
             
    
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # print("Updated Post contents: " + str(post))
    
    index = find_index(id)
    print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doesnt exist") 
    updated_dict = post.dict()
    updated_dict["id"] = id
    my_posts[index] = updated_dict
    return {"Data": updated_dict}