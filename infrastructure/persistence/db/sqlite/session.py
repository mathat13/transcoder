from sqlalchemy.orm import sessionmaker

from infrastructure.persistence.db.sqlite.engine import engine

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_session():
    """Application-level dependency."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()