Flask-Dance Example App: Google SQLAlchemy Edition
==================================================

This repository provides an example of how to use `Flask-Dance`_ with
a SQLAlchemy storage. This particular repository uses Google as an
OAuth provider, and it wires together the following Flask extensions:

* `Flask-Dance`_
* `Flask-SQLAlchemy`_
* `Flask-Login`_

You can run this code locally, or deploy it to Heroku_ to test it out.

|heroku-deploy|

Local Installation
``````````````````

Step 1: Get OAuth credentials from Google
-----------------------------------------
Visit the Google Developers Console at https://console.developers.google.com
and create a new project. In the "APIs & auth" section, click on "Credentials",
and then click the "Create a new Client ID" button. Select "Web Application"
for the application type, and click the "Configure consent screen" button.
Put in your application information, and click Save. Once you’ve done that,
you’ll see two new fields: "Authorized JavaScript origins" and
"Authorized redirect URIs". Set the authorized redirect URI to
``http://localhost:5000/login/google/authorized``, and click "Create Client ID".
Google will give you a client ID and client secret, which we'll use in step 4.

Step 2: Install code and dependencies
-------------------------------------
Run the following commands on your computer::

    git clone https://github.com/singingwolfboy/flask-dance-google-sqla.git
    cd flask-dance-google-sqla
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

These commands will clone this git repository onto your computer,
create a `virtual environment`_ for this project, activate it, and install
the dependencies listed in ``requirements.txt``.

Also note that if you have trouble installing ``psycopg2``, it's OK to
skip it. That dependency is only needed if you are using PostgreSQL
for your database, and if you're running locally, then you can use
SQLite instead, which is simpler. SQLite is also the default option,
so you don't need to reconfigure anything.

Step 3: Create the database
---------------------------
Since we're storing OAuth data in the SQLAlchemy storage, we need to
create the database to hold that data. Fortunately, this project includes
basic command line support, so doing so is pretty straightforward.
Run this code::

    flask createdb

If it worked, you should see the message "Database tables created".

Step 4: Set environment variables
---------------------------------
Many applications use `environment variables`_ for configuration, and
Flask-Dance is no exception. You'll need to set the following environment
variables:

* ``FLASK_APP``: set this to ``app``. Since this is the default value, you
  can leave it unset it you prefer.
* ``FLASK_SECRET_KEY``: set this to a random string. This is used for
  signing the Flask session cookie.
* ``GOOGLE_OAUTH_CLIENT_ID``: set this to the client ID
  you got from Google.
* ``GOOGLE_OAUTH_CLIENT_SECRET``: set this to the client secret
  you got from Google.
* ``OAUTHLIB_RELAX_TOKEN_SCOPE``: set this to ``true``. This indicates that
  it's OK for Google to return different OAuth scopes than requested; Google
  does that sometimes
* ``OAUTHLIB_INSECURE_TRANSPORT``: set this to ``true``. This indicates that
  you're doing local testing, and it's OK to use HTTP instead of HTTPS for
  OAuth. You should only do this for local testing.
  Do **not** set this in production! [`oauthlib docs`_]

The easiest way to set these environment variables is to define them in
an ``.env`` file. You can then install the `python-dotenv`_ package
to make Flask automatically read this file when you run the dev server.
This repository has a ``.env.example`` file that you can copy to
``.env`` to get a head start.

Step 5: Run your app and login with Google!
-------------------------------------------
If you're setting environment variables manually, run your app using the
``flask`` command::

    flask run

Then, go to http://localhost:5000/ to visit your app and log in with Google!

If your application isn't loading the environment variables from your ``.env``
file, then you need to install the `python-dotenv`_ package using ``pip``::

    pip install python-dotenv

Once the package is installed, try the ``flask run`` command again

.. _Flask: http://flask.pocoo.org/docs/
.. _Flask-Dance: http://flask-dance.readthedocs.org/
.. _Flask-SQLAlchemy: http://flask-sqlalchemy.pocoo.org/
.. _Flask-Login: https://flask-login.readthedocs.io
.. _Google: https://myaccount.google.com/
.. _Heroku: https://www.heroku.com/
.. _environment variables: https://en.wikipedia.org/wiki/Environment_variable
.. _oauthlib docs: http://oauthlib.readthedocs.org/en/latest/oauth2/security.html#envvar-OAUTHLIB_INSECURE_TRANSPORT
.. _python-dotenv: https://github.com/theskumar/python-dotenv
.. _virtual environment: https://docs.python.org/3.7/library/venv.html
.. _Fork this GitHub repo: https://help.github.com/articles/fork-a-repo/

.. |heroku-deploy| image:: https://www.herokucdn.com/deploy/button.png
   :target: https://heroku.com/deploy
   :alt: Deploy to Heroku
