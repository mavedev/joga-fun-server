from typing import Union, Dict, Any, AnyStr
from werkzeug.datastructures import Authorization

# Numbers.
TEXT_LEN_MAX = 255
TEXT_LEN_MID = 150
TEXT_LEN_MIN = 80
POSTS_CHUNK_SIZE = 5

# Aliases.
JSONLike = Dict[str, Any]
AuthHeader = Union[Dict[AnyStr, AnyStr], Authorization]
