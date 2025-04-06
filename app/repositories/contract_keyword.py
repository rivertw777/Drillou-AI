from sqlalchemy.orm import Session
from app.models.contract_keyword import ContractKeyword


class ContractKeywordRepository:
    @staticmethod
    def save(db: Session, model: ContractKeyword) -> ContractKeyword:
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    @staticmethod
    def get_by_id(db: Session, keyword_id: int) -> ContractKeyword:
        return db.query(ContractKeyword).filter(ContractKeyword.id == keyword_id).first()