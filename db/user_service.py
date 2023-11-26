from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker, Session
from db.models.user import User
from db.utils import session_decorator


class UserService:

    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)

    @session_decorator
    def get_user(self, telegram_id, session: Session):
        return session.query(User).filter_by(telegram_id=telegram_id).first()

    @session_decorator
    def add_user(self, telegram_id, session: Session):
        inserting_user = insert(User).values(telegram_id=telegram_id)
        session.execute(inserting_user)
