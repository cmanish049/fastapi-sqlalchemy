from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from db.databse import Base

class Product(Base):
    __tablename__ = "products"


    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(250))
    price: Mapped[float]
    quantity: Mapped[int]