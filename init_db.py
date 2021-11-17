import yaml
from sqlalchemy import create_engine

with open('./config/config.yaml') as file:
    config = yaml.safe_load(file)

database_info = config['database']
DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
ADMIN_DB_URL = DSN.format(
    user=database_info['admin_user'],
    password=database_info['admin_password'],
    database='postgres',
    host=database_info['host'],
    port=database_info['port']
)

admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')


def setup_db():
    conn = admin_engine.connect()
    conn.execute(f"DROP DATABASE IF EXISTS {database_info['name']}")
    conn.execute(f"CREATE DATABASE {database_info['name']} ENCODING 'UTF8'")
    conn.execute(f"GRANT ALL PRIVILEGES ON DATABASE {database_info['name']} TO {database_info['user']}")
    conn.close()


if __name__ == "__main__":
    setup_db()
