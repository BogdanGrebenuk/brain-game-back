python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ./app/alembic.ini.dist ./app/alembic.ini
cp ./config/config.yaml.dist ./config/config.yaml
echo "Don't forget to fill in all required data in config files."