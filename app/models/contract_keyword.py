from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class ContractKeyword(Base):
    __tablename__ = "contract_keywords"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    construction_type = Column(String(255), nullable=False)
    construction_cost = Column(String(255), nullable=False)
    start_date = Column(String(255), nullable=False)
    end_date = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self, client_id: int, construction_type: str, construction_cost: str, start_date: str, end_date: str):
        self.client_id = client_id
        self.construction_type = construction_type
        self.construction_cost = construction_cost
        self.start_date = start_date
        self.end_date = end_date
