import unittest
import os

import neocities

# Bonus: Running these tests enough times will likely get you banned!


class NeoCitiesTestCase(unittest.TestCase):
    def setUp(self):
        auth = (os.environ['NEOCITIES_USER'],
                os.environ['NEOCITIES_PASS'])
        self.nc = neocities.NeoCities(*auth)

    def test_info_no_auth(self):
        self.nc = neocities.NeoCities()
        response = self.nc.info('blog')
        self.assertEqual(response['result'], 'success')

    """
    Tests from this point on require you to have a NeoCities.org account
    """

    def test_info_auth(self):
        response = self.nc.info()
        self.assertEqual(response['result'], 'success')

    def test_upload_and_delete(self):
        """
        I would usually refrain from testing multiple things at once but order
        is very important in this case
        """
        response = self.nc.upload(('tests/fixtures/cat.png', 'neko.png'),
                                  ('tests/fixtures/gpl.html', 'gpl.html'))
        self.assertEqual(response['result'], 'success')
        response = self.nc.delete('neko.png', 'gpl.html')
        self.assertEqual(response['result'], 'success')
