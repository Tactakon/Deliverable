# pylint: disable=invalid-name
"""
Module for testing user playlist queries.

Defines a `TestMyModule` class that contains test cases for functions related to
user playlists. The tests use a mock database and cover scenarios such as retrieving
playlists by user ID. To run the tests, execute this module as a script using the
`unittest` module.
"""
import unittest
from flask import Flask
from main import db, Users, Playlists, get_playlists_by_user_id

class TestMyModule(unittest.TestCase):
    """
    Test class for user playlist queries.

    This class contains test cases for functions related to user playlists, such as
    retrieving playlists by user ID. The tests use a mock database to avoid modifying
    the production database. The test database is created and populated with some
    test data during the `setUp()` method, and deleted during the `tearDown()` method.
    """
    def setUp(self):
        """
        Renders the create playlist page and handles the creation of new playlists.

        Returns:
            If the request method is GET, a rendered HTML template of the create playlist page.
            If the request method is POST and the playlist was created successfully,
            a redirect to the playlist page.
            Otherwise, a rendered HTML template of the create playlist page with an error message.
        """
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mockDatabase.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db
        self.db.init_app(self.app)
        db.create_all()

        # Add some test data to the database
        user1 = Users(email='user1@test.com',
                      username='user1', password='password1')
        user2 = Users(email='user2@test.com',
                      username='user2', password='password2')
        user4 = Users(email='user4@test.com',
                      username='user4', password='password4')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user4)

        playlist1 = Playlists(name='playlist1', password='playlist1password',
                              songs='song1,song2,song3', creator=user1.id)
        playlist2 = Playlists(name='playlist2', password='playlist2password',
                              songs='song4,song5,song6', creator=user2.id)

        db.session.add(playlist1)
        db.session.add(playlist2)

        db.session.commit()

    def tearDown(self):
        """
        Tear down the test environment for the TestMyModule class.

        This function removes the test database created during setup.
        It drops all tables in the database and clears the database session.

        Returns:
        None
        """

        # Drop the test database
        db.session.remove()
        db.drop_all()

    def test_get_playlists_by_user_id(self):
        """
        Test `get_playlists_by_user_id()` function.

        Adds a playlist associated with user ID 1 to the database, calls the function with
        that user ID, and checks that the expected playlist is returned.

        Returns:
            None
        """
        # Add a playlist associated with user ID 1
        playlist = Playlists(name='playlist1', password='password1',
                             songs='song1,song2', creator=1)
        db.session.add(playlist)
        db.session.commit()

        # Call the function and check the result
        actual_playlists = get_playlists_by_user_id(1)
        expected_playlists = [playlist]
        self.assertEqual(actual_playlists, expected_playlists)

if __name__ == '__main__':
    unittest.main()
