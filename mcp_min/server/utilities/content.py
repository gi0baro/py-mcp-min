import json
from itertools import chain

import pydantic_core

from ... import types
from .types import Image


def convert_to_content(result):
    if result is None:
        return []

    if isinstance(result, types.TextContent | types.ImageContent | types.EmbeddedResource):
        return [result]

    if isinstance(result, Image):
        return [result.to_image_content()]

    if isinstance(result, list | tuple):
        return list(chain.from_iterable(convert_to_content(item) for item in result))

    if not isinstance(result, str):
        try:
            result = json.dumps(pydantic_core.to_jsonable_python(result))
        except Exception:
            result = str(result)

    return [types.TextContent(type="text", text=result)]
