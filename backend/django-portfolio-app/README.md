# Django Portfolio Project

## How to run

```bash
poetry install
make serve

# visit http://localhost:8000
```

## Django development flow

```bash
# Virtual environment setup
poetry init
poetry add django
poetry shell

# Create a new project
django-admin startproject portfolio

# Create a new app, add it in the "INSTALLED_APPS" of the project settings (personal_portfolio/settings.py)
python manage.py startapp pages

# Create a html for the app (view)
# Add the html to the pages/view.py with path "pages/home.html"
mkdir -p pages/templates/pages
touch pages/templates/pages/home.html

# Create the App URL and add it to the project URL (personal_portfolio/urls.py)
touch pages/urls.py

# Run the server
python manage.py runserver
```

## Django ORM

```bash
# Create a model in the app_name/models.py

# Run the migration generate command
python manage.py makemigrations app_name

# Apply the migration, a table will be created in the sqlite database
python manage.py migrate
```

## References

[Get Started With Django: Build a Portfolio App – Real Python](https://realpython.com/get-started-with-django-1/)
