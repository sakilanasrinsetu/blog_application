from django.test import TestCase
from rest_framework.test import APITestCase
from faker import Faker
from rest_framework import status


# Create your tests here.

class PostTest(APITestCase):

    # For All Post Get
    def test_get_post(self):
        _response = self.client.get('/blog/post/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 200)

    # For Post Create

    def test_post_post(self):
        _response = self.client.post('/blog/post/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 401)

    # For Post Update

    def test_patch_post(self):
        _response = self.client.patch('/blog/post/2/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 401)

    # For Post Delete

    def test_delete_post(self):
        _response = self.client.delete('/blog/post/2/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 401)

    # For Post Details Get

    def test_get_post(self):
        _response = self.client.get('/blog/post/2/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 200)


class CommentTest(APITestCase):

    # For All Comment Get
    def test_get_comment(self):
        _response = self.client.get('/blog/comment/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 200)

    # For Post Comment

    def test_post_comment(self):
        _response = self.client.post('/blog/comment/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 401)

    # For Post Update

    def test_patch_comment(self):
        _response = self.client.patch('/blog/comment/2/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 401)

    # For Post Delete

    def test_delete_post(self):
        _response = self.client.delete('/blog/comment/2/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 401)

    # For Post Details Get

    def test_get_comment(self):
        _response = self.client.get('/blog/comment/2/', format="json")
        _data = _response.json()
        self.assertEqual(_response.status_code, 200)

