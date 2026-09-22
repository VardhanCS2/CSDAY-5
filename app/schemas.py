from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    field_validator,
    model_validator
)


# =========================
# USER SCHEMAS
# =========================

class UserCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    age: int = Field(
        ge=18,
        le=100
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        return value


class UserUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: EmailStr | None = None

    age: int | None = Field(
        default=None,
        ge=18,
        le=100
    )


class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    email: EmailStr
    age: int


# =========================
# PRODUCT SCHEMAS
# =========================

class ProductCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    price: float = Field(
        gt=0
    )

    user_id: int = Field(
        gt=0
    )


class ProductUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    price: float | None = Field(
        default=None,
        gt=0
    )


class ProductResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    description: str | None
    price: float
    user_id: int


# =========================
# NESTED PRODUCT RESPONSE
# =========================

class ProductOwner(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str


class ProductWithOwner(ProductResponse):

    owner: ProductOwner