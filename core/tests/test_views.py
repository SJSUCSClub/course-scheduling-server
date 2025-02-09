from django.test import TestCase
from django.urls import reverse

class TestViews(TestCase):
    def test_get_review_view(self):
        response = self.client.get(reverse('get_review', kwargs={'review_id': '1'}))

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['professor_id'], 'aj.faas')