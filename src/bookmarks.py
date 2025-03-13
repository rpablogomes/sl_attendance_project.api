from flask import Blueprint

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

@bookmarks.get("/")
def register():
    return "User created"

@bookmarks.post("/me")
def tet():
    return "me"