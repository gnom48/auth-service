from typing import Any
from pydantic import BaseModel, Field


class ResultResponseBody(BaseModel):
    res: Any = Field(default=None)
