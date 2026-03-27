from pydantic import BaseModel, Field

class VanillaComponentSpec(BaseModel):
    componentName: str = Field(...)
    html: str = Field(
        ...,
        description="Pure semantic HTML. No Angular syntax, no framework directives."
    )
    css: str = Field(
        ...,
        description="Pure CSS. No :host, no ::ng-deep, no Angular-specific selectors."
    )
    ts: str = Field(
        ...,
        description="Vanilla JavaScript only. No imports, no classes, no TypeScript types. Must run directly in a browser <script> tag."
    )