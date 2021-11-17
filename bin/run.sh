source venv/bin/activate
cd app
PYTHONPATH='..' alembic upgrade head
cd ../tests
PYTHONPATH='..' python -m unittest
cd ..
nohup python -m app