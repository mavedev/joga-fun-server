from typing import List

from app.model import Post


class PostChunkDTO:
    def __init__(self, total: int, posts: List[Post]) -> None:
        self.total = total
        self.posts = posts
