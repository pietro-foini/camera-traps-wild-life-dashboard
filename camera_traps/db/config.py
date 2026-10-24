from camera_traps.db.postgres import PostgresHandler
from camera_traps.settings import S

db = PostgresHandler(
    db_user=S.DB_USER,
    db_password=S.DB_PASSWORD,
    db_host=S.DB_HOST,
    db_port=S.DB_PORT,
    db_name=S.DB_NAME,
)
