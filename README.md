python --version

pip install django
pip install -r requirements.txt
python -m venv venv 
source venv/bin/activate
python manage.py runserver

#create new application (venv):   python manage.py startapp cevaunic

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
