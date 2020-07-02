from typing import Union, Dict, Any, AnyStr
from werkzeug import Authorization

# Numbers.
_TEXT_LEN_MAX: int = 255
_TEXT_LEN_MID: int = 150
_TEXT_LEN_MIN: int = 80

# ALiases.
JSONLike = Dict[str, Any]
AuthHeader = Union[Dict[AnyStr, AnyStr], Authorization]
