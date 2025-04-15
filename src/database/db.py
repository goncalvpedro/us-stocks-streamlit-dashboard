from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

# DB config
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DATABASE_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)
    shares = Column(Numeric(10, 3), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    first_acquisition = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Portfolio(symbol='{self.symbol}', shares={self.shares})>"

    @classmethod
    def create_table(cls):
        try:
            Base.metadata.create_all(bind=engine)
            print("Table ready to go.")
        except SQLAlchemyError as e:
            print(f"Unable to create table due to an error: {e}")

    @classmethod
    def create_item(cls, symbol, shares, price, first_acquisition):
        cls.create_table()
        session = SessionLocal()
        try:
            item = cls(symbol=symbol, shares=shares, price=price, first_acquisition=first_acquisition)
            session.add(item)
            session.commit()
            print(f"Item created successfully.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Unable to create item due to an error: {e}")
        finally:
            session.close()

    @classmethod
    def read_portfolio(cls):
        session = SessionLocal()
        try:
            return session.query(cls).all()
        except SQLAlchemyError as e:
            print(f"Unable to read portfolio due to an error: {e}")
        finally:
            session.close()

    @classmethod
    def update_item(cls, symbol, shares):
        session = SessionLocal()
        try:
            item = session.query(cls).filter_by(symbol=symbol).first()
            if item:
                item.shares = shares
                session.commit()
                print(f"Item {symbol} updated successfully.")
            else:
                print(f"Item {symbol} not found.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Unable to update item {symbol} due to an error: {e}")
        finally:
            session.close()

    @classmethod
    def delete_item(cls, symbol):
        session = SessionLocal()
        try:
            item = session.query(cls).filter_by(symbol=symbol).first()
            if item:
                session.delete(item)
                session.commit()
                print(f"Item {symbol} deleted successfully.")
            else:
                print(f"Item {symbol} not found.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Unable to delete item {symbol} due to an error: {e}")
        finally:
            session.close()
