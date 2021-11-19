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
  - finishing existing session due to completion/failure 👍/👎
  - canceling session 🛑
- Comparing images for similarity (as part of one mini-game) 👀

### External API used
[DeepAI API](https://deepai.org/machine-learning-model/image-similarity) has been used for comparing images and figuring out its similarity.

### API
```
Action: Register user
  
Route: /register
  
Method: POST

Body fields:
- email: string
- username: string
- password: string

Response:
- id: string
- username: string
- email: string
- number: integer
```

```
Action: Authenticate user

Route: /login

Method: POST

Body fields:
- email: string
- password: string

Response:
- token: string
```

```
Action: Logout user

Route: /logout

Method: POST

Headers:
- Authorization: Bearer <token>
```


```
Action: Get "me" info

Route: /api/users/me

Method: GET

Headers:
- Authorization: Bearer <token>

Response:
- id: string
- username: string
- email: string
- number: integer
```

```
Action: Get info about last session

Route: /api/sessions/last

Method: GET

Headers:
- Authorization: Bearer <token>

Response:
- sessionId: string|null (null in the case of the absence of any session)
- sessionStatus: integer|null 
- sessionStage: integer|null
- sessionTotalScore: integer|null
- sessionDifficulty: integer|null
```

```
Action: Start new session

Route: /api/sessions

Method: POST

Headers:
- Authorization: Bearer <token>

Response:
- sessionId: string
- sessionStatus: integer 
- sessionStage: integer
- sessionTotalScore: integer
- sessionDifficulty: integer
```

```
Action: Notify about stage completion

Route:  /api/sessions/last/complete

Method: POST

Headers:
- Authorization: Bearer <token>

Body:
- score: integer

Response:
- sessionId: string
- sessionStatus: integer 
- sessionStage: integer
- sessionTotalScore: integer
- sessionDifficulty: integer
```

```
Action: Notify about failure

Route: /api/sessions/last/close

Method: POST

Headers:
- Authorization: Bearer <token>

Body:
- score: integer

Response:
- sessionId: string
- sessionStatus: integer 
- sessionStage: integer
- sessionTotalScore: integer
- sessionDifficulty: integer
```

```
Action: Cancel session

Route: /api/sessions/last/cancel

Method: POST

Headers:
- Authorization: Bearer <token>

Response:
- sessionId: string
- sessionStatus: integer 
- sessionStage: integer
- sessionTotalScore: integer
- sessionDifficulty: integer
```

```
Action: Get leaderboard

Route: /api/leaderboard

Method: GET

Headers:
- Authorization: Bearer <token>

Response:
- <position>:string : {
      username: string, 
      email: string, 
      totalScore: integer, 
      totalScore: boolean,
      number: integer
  }
```

```
Action: Compare images

Route: /api/images/compare

Method: POST

Headers:
- Authorization: Bearer <token>

Body:
- originalImage: string (base64)
- drawnImage: string (base64)

Response: 
- distance: integer
```

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