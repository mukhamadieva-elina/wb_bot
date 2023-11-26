from sqlalchemy.orm import sessionmaker, Session
from db.models.product import Product
from db.models.user import User
from db.utils import session_decorator


class UserService:

    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)

    @session_decorator
    def get_user(self, telegram_id, session: Session):
        return session.query(User).filter_by(telegram_id=telegram_id).first()

    @session_decorator
    def addUser(self, user: User, session: Session):
        session.add(user)



