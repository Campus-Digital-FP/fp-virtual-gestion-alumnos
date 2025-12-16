import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from logger_config import logger   # tu logger personalizado

# Cargar variables de entorno
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear engine y sesión
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

logger.info("Conexión SQLAlchemy a Moodle configurada.")


# ---------- Ejemplo de consulta con logs ----------
def get_usuarios_activos(limit: int = 10):
    """
    Devuelve lista de tuplas (username, firstname, lastname, lastaccess)
    de usuarios activos en Moodle.
    """
    logger.debug(f"Consultando {limit} usuarios activos...")
    sql = text("""
        SELECT username, firstname, lastname, lastaccess
        FROM mdl_user
        WHERE deleted = 0 AND suspended = 0
        ORDER BY lastaccess DESC
        LIMIT :lim
    """)
    try:
        with engine.connect() as conn:
            rows = conn.execute(sql, {"lim": limit}).fetchall()
        logger.info(f"Se recuperaron {len(rows)} usuarios activos.")
        logger.markdown(f"Consulta exitosa: {len(rows)} usuarios activos recuperados.")
        return rows
    except Exception as e:
        logger.error(f"Error al consultar usuarios activos: {e}")
        raise


# ---------- Ejemplo con sesión ORM (reflexión) ----------
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
Base.prepare(autoload_with=engine)
MdlUser = Base.classes.mdl_user


def get_user_by_username(username: str):
    """
    Devuelve el objeto ORM de un usuario dado su username.
    """
    logger.debug(f"Buscando usuario '{username}'...")
    session = SessionLocal()
    try:
        user = session.query(MdlUser).filter_by(username=username).first()
        if user:
            logger.info(f"Usuario encontrado: {user.firstname} {user.lastname}")
            logger.markdown(f"Usuario **{username}** encontrado: {user.firstname} {user.lastname}")
        else:
            logger.warning(f"Usuario '{username}' no encontrado.")
        return user
    except Exception as e:
        logger.error(f"Error al buscar usuario '{username}': {e}")
        raise
    finally:
        session.close()