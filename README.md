# Gallery Images | Multi User

### Setup :
```bash
# create virtual environment
python -m venv venv

# clone repository
git clone https://github.com/Ahmed-mzn/gallery.git

# activate environment
# linux & mac :
source venv\bin\activate
#windows
venv\scripts\activate

# create .env file and copy .env-example content on it
# linux & mac | in windows create file manual
cd gallery
touch .env

# install requirements
pip install -r requirements.txt

# run migrations
python manage.py migrate

# runserver end enjoy
py python manage.py runserver
```