import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    # create and open a tempfile, returning a descriptor and path
    # and creates the database there.
    # Afterwards the tempfile is removed
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
# test the client without running the server
def client(app):
    return app.test_client()

@pytest.fixture
# calls the click commands registered with application
def runner(app):
    return app.test_cli_runner()

