python --version

echo 'Creating python virtual enviroment...'
python -m venv venv
source venv/bin/activate

echo 'Installing required packages...'
pip install -r requirements.txt

echo 'Starting Django server...'
python manage.py runserver 0.0.0.0:8000