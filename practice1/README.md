# Q12 football players

## Run

From `DjangoPractice`:

```bash
source .venv/bin/activate
cd practice1
python manage.py runserver
```

Open http://127.0.0.1:8000/. Stop the other practice project's server first if
it already uses port 8000, or run this one with `python manage.py runserver 8001`.

## Study order

1. `myapp/models.py`: Human, Goalkeeper and FieldPlayer are ordinary Python classes.
   Player is the only Django model. It stores both player types in one table.
2. `myapp/forms.py`: one ModelForm. Its extra `score` input means shots stopped
   for a goalie or goals for a field player. The view places it in the correct field.
3. `myapp/views.py`: register, display, searchplayer and findbest match the four
   operations in the question. The view raises and catches the required custom
   exceptions and passes messages to message.html.
4. `myapp/urls.py` connects views to the links in start.html.

Player IDs are entered by the user and must be unique numbers from 10000 to 99999.
Goalie stop rate is shots stopped / matches. A player with zero matches gets rate 0
to avoid division by zero. When best-player scores tie, the lowest ID is shown.
Unused statistics stay 0 in the database and display as a dash in the table.

## Existing records

The migration preserves records from the old Goalkeeper and FieldPlayer tables
before removing those tables. Old IDs outside the five-digit range, or duplicate
IDs from separate tables, receive new IDs starting at 10000.
This migration is a one-time conversion; the exam application code does not need
this conversion logic when starting from a fresh Player model.

## Checks

```bash
python manage.py check
python manage.py test myapp
```
