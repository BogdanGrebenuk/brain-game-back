import asyncio

import aiopg.sa
import nest_asyncio


def init_engine(database_config):
    nest_asyncio.apply()
    loop = asyncio.get_running_loop()
    engine = loop.run_until_complete(
        aiopg.sa.create_engine(
            database=database_config['name'],
            user=database_config['user'],
            password=database_config['password'],
            host=database_config['host'],
            port=database_config['port']
        )
    )
    yield engine
    engine.close()
    loop.run_until_complete(engine.wait_closed())
