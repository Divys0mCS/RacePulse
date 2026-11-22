from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings
from app.database.connection_args import get_connect_args


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args=get_connect_args(),
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)