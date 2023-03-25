import unittest
from flask import Flask
from main import app, db, Users, Playlists, AddUserToDB
from werkzeug.security import check_password_hash


class TestMyModule(unittest.TestCase):
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

    def testAddUser(self):
        """
        Test the AddUserToDB function.

        This function tests the functionality of the AddUserToDB function.
        It creates a new user, adds them to the database, and then retrieves the user from the database.
        It checks that the user was added correctly and that their password is properly hashed.
        It also tests adding a user with an existing email.

        Returns:
        None
        """

        # Create a new user and add them to the database
        AddUserToDB(email='user3@test.com',
                    username='user3', password='password3')

        # Retrieve the user from the database
        user = Users.query.filter_by(email='user3@test.com').first()

        # Check that the user was added correctly
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'user3')
        self.assertTrue(check_password_hash(user.password, 'password3'))

        # Test adding a user with an existing email
        result = AddUserToDB(email='user1@test.com',
                             username='user4', password='password4')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
