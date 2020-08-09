from typing import List

from app.model import Post


class PostChunkDTO:
    def __init__(self, chunks_left: int, posts: List[Post]) -> None:
        self.chunks_left = chunks_left
        self.posts = posts
