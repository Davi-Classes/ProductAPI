from config import settings
from sqlalchemy import create_engine, BigInteger, Integer
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
    except:
        session.rollback()
    finally:
        session.close()

# Definindo nossa classe BaseModel que utilizaremos 
# para definir nossas entidades
class BaseModel(DeclarativeBase): 
    pass

# Criando Tipo "Long" que é um BigInt mas que será um Int para o sqlite
Long = BigInteger().with_variant(Integer(), 'sqlite')
