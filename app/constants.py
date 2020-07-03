from typing import Union, Dict, Any, AnyStr
from werkzeug.datastructures import Authorization

# Numbers.
_TEXT_LEN_MAX = 255
_TEXT_LEN_MID = 150
_TEXT_LEN_MIN = 80
JWT_EXP_DELTA_SECONDS = 20
JWT_ALGORITHM = 'HS256'

# Aliases.
JSONLike = Dict[str, Any]
AuthHeader = Union[Dict[AnyStr, AnyStr], Authorization]
