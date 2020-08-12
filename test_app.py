import app
import unittest
import flask


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_scrape_by_url(self):
        with self.app as client:
            # resp = client.post('/url-based', data=dict(text="https://google.com"))
            # self.assertEqual(200, resp.status_code)
            client.get('/url-based')
            self.assertIn("Enter the Article URL", app.scrape_by_url())

if __name__ == '__main__':
    unittest.main()
    