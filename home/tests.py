from django.test import TestCase
from .models import *

# Create your tests here.
class TopicModelTest(TestCase):
    def test_topic_model_exists(self):
        topics = Topic.objects.count()

        self.assertEquals(topics, 0) 