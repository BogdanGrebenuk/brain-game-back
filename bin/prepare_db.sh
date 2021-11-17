source venv/bin/activate
python init_db.py
cd app
PYTHONPATH='..' alembic upgrade head
