# Practice 3 - Lab Asset Registry

Simple function-based views, using the same form/POST/save/redirect style as practice2.
The app is named `assets`, as required by the question.

## Run

From DjangoPractice/practice3:

```bash
../.venv/bin/python manage.py createsuperuser
../.venv/bin/python manage.py runserver 8003
```

Log in at http://127.0.0.1:8003/admin/ then open
http://127.0.0.1:8003/assets/ in the same browser.
The question requires authorized staff, so each view starts with a simple
`request.user.is_staff` check. No custom login page is needed.

The database migrations have already been applied. For a fresh database run:

```bash
../.venv/bin/python manage.py migrate
```

## Read in this order

1. assets/models.py - fields, unique asset ID and automatic creation time.
2. assets/forms.py - ModelForm excluding created_at; a date picker for purchase_date.
3. assets/views.py - register, display and delete.
4. assets/urls.py - app_name='assets' gives names such as assets:list.
5. assets/templates/assets/ - the three required templates.

GET on the delete URL shows confirmation. POST deletes the asset and redirects
to the list. `messages.success()` survives the redirect; the list template displays it.
`order_by('-created_at')` displays newest assets first.

There is no update view. The optional detail page is omitted to keep the app small.
Category and location are text inputs. Status is Active or Decommissioned.

## Check

```bash
../.venv/bin/python manage.py check
../.venv/bin/python manage.py test assets
```
