=====
Locations
=====

Locations is a simple Django app to add and manages tracks made out of locations.

Quick start
-----------

1. Add "locations" to your INSTALLED_APPS setting:

    INSTALLED_APPS = [
        ...
        'locations',
		django_filters,
    ]

2. Include the feeds URLconf in your project urls.py like this::

    path('locations/', include('locations.urls')),

3. Run `python manage.py migrate` to create the feeds models.

4. Start the development server and visit http://127.0.0.1:8000/admin/