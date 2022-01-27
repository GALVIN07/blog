from urllib import response
from django.test import TestCase
from .models import Post
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.
class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email= 'test@email.com',
            password= 'secret'

        )
        self.post = Post.objects.create(
            title="A test", 
            body= "Test", 
            author= self.user
        )
    def test_post_list_view(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A test")

    def test_post_create_view(self):
        response = self.client.post(reverse("post_new"), {
            "title": "New title",
            "body": "New body",
            "author": self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New title")
        self.assertEqual(Post.object.last().body, "New body")
        self.assertTemplateNotUsed(response, "blog/new.html")


    def test_body_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f"{post.body}"
        self.assertEqual(expected_object_name, "Test")

    def test_post_string_representation(self):
        post = Post.objects.get(id=1)
        str_repr = str(post)
        self.assertEqual(str_repr, "A test")

class PostViewTest(TestCase):
    def setUp(self):
        Post.objects.create(title="Another test", body= "Test2")

    def test_detailview_contains_content(self):
        resp = self.client.get(reverse("post_detail", args=[1]))
        self.assertContains(resp, "Another test")

    def test_postview_uses_correct_template(self):
        resp = self.client.get("/posts/")
        self.assertTemplateUsed(resp, "posts/list.html")

class PostCreateTest(TestCase):
    def setUp(self):
        Post.objects.create(title="Another test", body= "Test3")

    def test_postcreate_contains_content(self):
        resp = self.client.get(reverse("post_detail", args=[1]))
        self.assertContains(resp, "Another test")

    def test_postcreate_uses_correct_template(self):
        resp = self.client.get("/posts/new")
        self.assertTemplateUsed(resp, "posts/new.html")

class PostDetailTest(TestCase):
    def setUp(self):
        Post.objects.create(title="Yet Another test", body= "Test4")

    def test_detailview_uses_correct_template(self):
        resp = self.client.get("/posts/")
        self.assertTemplateUsed(resp, "posts/detail.html")


