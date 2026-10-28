# Building promoter lab

The existing Student model, page and root URL are retained. The building app uses
the same `mapp` app and the existing SQLite database configuration in `proj`.

## Run

From the PythonPractice folder:

```bash
source .venv/bin/activate
cd proj
python manage.py migrate
python manage.py seed_apartments
python manage.py runserver
```

Open http://127.0.0.1:8000/buildingapp/home

If setting up a fresh environment first run `python -m pip install -r requirements.txt`
from PythonPractice. To access apartment management, run
`python manage.py createsuperuser` and open http://127.0.0.1:8000/admin/.

## What to study, in order

1. `models.py`: Apartment represents a floor, Registration represents a customer allocation.
2. `forms.py`: ModelForm builds the five customer fields from Registration.
   `clean_mobile_number()` checks exactly ten ASCII digits; phone numbers stay strings.
3. `views.py`: GET builds an empty form. POST binds the submitted data.
   `is_valid()` runs validation; `save(commit=False)` creates an unsaved model object.
   The view chooses the floor, checks availability, computes cost, then calls `save()`.
4. `Registration.html`: `form.as_p` renders fields and validation errors.
5. `urls.py`: URLs connect browser requests to views; template URL tags build links.

## Fixed rules and sample data

| Flat type | Floor | Area |
|---|---|---|
| 3 BHK | 0 | 1200 sq. ft. |
| 2 BHK | 1 | 1000 sq. ft. |
| 1 BHK | 2 | 800 sq. ft. |

Cost = area × price per square foot. The saved cost is the allocation-time price.
The seed command adds five sample complexes with three floors each, five flats on
each floor and sample prices. Names, addresses, counts and prices are assumptions
because the question does not provide them. Re-running the command preserves data.
The five sample complex names are listed in `APARTMENT_NAMES` in models.py.
Both the admin and registration form display these names as a dropdown.

## CRUD map

| Operation | View | Template |
|---|---|---|
| Create customer | register_flat | Registration.html |
| Read all inventory | display_apartments | Apartment.html |
| Read all customers | display_registrations | Customer.html |
| Read one customer | receipt | Receipt.html |
| Update customer | edit_registration with form instance | Registration.html |
| Delete customer | delete_registration, POST only | Button in Customer.html |
| Apartment CRUD | Django admin | Built-in admin pages |

Editing contact details keeps allocation and price unchanged. Moving to a different
flat type or complex releases the old flat and reserves a new one. Deletion releases
the allocated flat. Counts use simple Python arithmetic and `.save()`.
Create and Update have separate functions so each can be studied independently.
`get_floor()` and `get_area()` use ordinary if/elif/else statements for the fixed rules.
There are no custom decorators, transactions, Q/F expressions or regular expressions
in this exam version. It assumes sequential local use and successful database writes;
transactions and concurrency controls would be needed for a production booking system.

Use the customer pages for registration changes so inventory stays in sync.
Complex name plus floor identifies an allocation: do not rename or remove an
inventory row while it has customer registrations. This is a simplified lab app
with public customer CRUD pages, intended for local exam practice.

## Verify

```bash
python manage.py check
python manage.py test mapp
```

The four required paths have no trailing slash:
`/buildingapp/home`, `/buildingapp/registerFlat`, `/buildingapp/dispApartment`,
`/buildingapp/dispRegistration`. Extra paths support edit, delete and receipts.
