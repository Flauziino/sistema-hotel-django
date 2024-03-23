from django.test import TestCase
from django.urls import reverse


class HospedesURLsTest(TestCase):

    def test_hospedes_realizar_rezerva_url_is_correct(self):
        url = reverse('hospedes:realizar_reserva')
        self.assertEqual(
            url, '/realizar-reserva/'
        )

    def test_hospedes_check_in_url_is_correct(self):
        url = reverse(
            'hospedes:check_in',
            kwargs={'id': 1}
        )
        self.assertEqual(
            url, '/hospede-info/1/check-in'
        )

    def test_hospedes_check_out_url_is_correct(self):
        url = reverse(
            'hospedes:check_out',
            kwargs={'id': 1}
        )
        self.assertEqual(
            url, '/hospede-info/1/check-out'
        )
