import sqlalchemy as sa
import sqlalchemy.orm as sao

import project_config as configs

BIND = sa.create_engine(
    configs.get_postgres_uri(),
    isolation_level="REPEATABLE READ",
)

DEFAULT_SESSION_FACTORY = sao.sessionmaker(bind=BIND)
