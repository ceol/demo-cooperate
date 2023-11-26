# Demo for Cooperate Marketing

A small, unstyled Django app.

# Usage

## Installation

If you have pipenv
```
pipenv install
pipenv shell
```

Or, without pipenv
```
pip install -r requirements.txt
```

Then
```
python manage.py migrate
python manage.py runserver 8080
```

And visit [http://127.0.0.1:8080/](http://127.0.0.1:8080/) to view the app.

# Design Decisions

* Ads are stored as rows in a SQLite table. I think this is a great use case for a relational database, since it appears to have relations to other data (e.g. the spender, where it's running). A graph or key-value store could also work, maybe indexed by who created it (`site_id` or `user_id`).

* Cost sharing rate is stored alongside each ad, even though the spec did not indicate it could change. It's very possible the rate could change regardless, so having that historical information is important. This also makes it possible to use the database to make calculations.
