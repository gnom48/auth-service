from typing import List
from pydantic import BaseModel, field_validator


class CatalogOrm:
    prop0: str
    prop01: str = "fergerg"
    prop02: int = 10

    def __init__(self, prop0: str):
        self.prop0 = prop0


class ModelOrm:
    prop1: int
    prop2: str
    prop3: List[CatalogOrm]

    def __init__(self, prop1: int, prop2: str, prop3: List[CatalogOrm]):
        self.prop1 = prop1
        self.prop2 = prop2
        self.prop3 = prop3

# -----------------------


class CatalogPydantic(BaseModel):
    prop0: str


class ModelPydantic(BaseModel):
    prop1: int
    prop2: str
    prop3: List[CatalogPydantic]

    @field_validator("prop3")
    def convert_catalog_orm_to_pydantic(cls, v):
        if isinstance(v, CatalogOrm):
            return CatalogPydantic(model_validate=v.__dict__)
        return v


mo = ModelOrm(prop1=100500, prop2="aaaaaa", prop3=[
              CatalogOrm("a1"), CatalogOrm("a2"), CatalogOrm("a3"),])

mp = ModelPydantic.model_validate(mo)

print(mp)
