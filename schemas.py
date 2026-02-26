from pydantic import BaseModel, Field
from typing import Literal

class AngularComponentSpec(BaseModel):
    componentName: str = Field(...)
    html: str = Field(...)
    css: str = Field(...)
    ts: str = Field(...)
    framework: Literal["angular"] = "angular"