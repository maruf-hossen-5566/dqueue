from app.db.session import SessionLocal


def get_db():
    """Create and close a database session"""
    db = SessionLocal()

    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
