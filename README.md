## Back-end for "Brain Game" project (test task for INT20H hackathon of KNKG team)

### What is inside?
- [aiohttp](https://docs.aiohttp.org/en/stable/) as an asynchronous framework 🚀
- [aiopg](https://aiopg.readthedocs.io/en/stable/) for accessing PostgreSQL from asyncio 🐘
- [sqlalchemy](https://www.sqlalchemy.org/) (core) for SQL queries generation 🍻
- [alembic](https://alembic.sqlalchemy.org/en/latest/) for manipulating migrations 🏃
- [marshmallow](https://marshmallow.readthedocs.io/en/stable/) for validation 🍭
- [dependency_injector](https://python-dependency-injector.ets-labs.org/) as a DI tool 🤖
- [pyjwt](https://pyjwt.readthedocs.io/en/latest/index.html) for auth flow 👋

### What can it do?
- Simple token-based auth flow 🧑
- Tracking user in-game progress 👁️
- Providing leaderboard 🏆
- Manipulating user game sessions 🔍
  - starting new game session 📱
  - moving user to the next stages of the game 🔝
  - finishing existing session due to completion/failure 👍
  - canceling session 🛑
- Comparing images for similarity (as part of one mini-game) 👀

### External API used:
[DeepAI API](https://deepai.org/machine-learning-model/image-similarity) has been used for comparing images and figuring out its similarity.

### Project structure
Domain-related code base is split into three packages:
- auth package (for auth flow)
- user package (for user-related flow)
- game package (for game-related flow)


### Deployment
1. Install PostgreSQL server (PostgreSQL 12.9 is recommended)
2. Install Python (Python3.7 is recommended)
3. Create virtual environment: `python3 -m venv venv`
4. Activate environment: `source venv/bin/activate`
5. Install packages: `pip install -r requirements.txt`
6. Set and fill with appropriate values config files: `cp ./app/alembic.ini.dist ./app/alembic.ini; cp ./config/config.yaml.dist ./config/config.yaml`
7. Initiate database: `python init_db.py`
8. Run migrations: `cd app; PYTHONPATH='..' alembic upgrade head; cd ../`
9. Run tests: `cd tests; PYTHONPATH='..' python -m unittest; cd ../`
10. Run server: `python -m app`