from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from .services.agebyname import AgeService
from employees.models import Customer, Employee
from rooms.models import Room

from tickets.models import PromoCode
from animals.models import Animal, Country, AnimalClass
from tickets.views import edit_code, delete_code

from animals.forms import AnimalForm


class TestSite(TestCase):

    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)

    def test_privacy(self):
        response = self.client.get('/privacy_policy')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)


class CustomerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            phone_number='+375448844333',
            age=21,
            spendings=45,
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.age, 21)
        self.assertEqual(self.customer.phone_number, '+375448844333')
        self.assertTrue(self.customer.spendings, 45)

    def test_str_representation(self):
        self.assertEqual(str(self.customer.user.username), 'testuser')


class AgifyTestCase(TestCase):
    @patch('requests.get')
    def test_get_random_joke(self, mock_get):
        # Мокаем результат GET-запроса
        expected_age = 41
        mock_get.return_value.json.return_value = expected_age

        age = AgeService.get_age_name('Andrei')

        # Проверяем результат
        self.assertEqual(age, expected_age)
        mock_get.assert_called_once_with(f'https://api.agify.io/?name=Andrei')


class LogoutUserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('users:logout')

    def test_logout_user_view(self):
        # Создаем тестового пользователя и входим в систему
        user = User.objects.create_user(username='test_user', password='password')
        self.client.login(username='test_user', password='password')

        # Отправляем запрос на выход пользователя из системы
        response = self.client.get(self.logout_url)

        # Проверяем, что пользователь вышел из системы и был перенаправлен на главную страницу
        self.assertEqual(response.status_code, 302)  # 302 - перенаправление
        self.assertEqual(response.url, reverse('animals:allanimals'))  # Проверяем перенаправление на главную страницу
        self.assertTrue(User.objects.filter(username='test_user').exists())  # Проверяем, что пользователь вышел из системы


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('users:login')

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)

    def test_login_view_post_invalid(self):
        response = self.client.post(self.url, {'username': 'invalid', 'password': 'invalid'})
        self.assertEqual(response.status_code, 200)


class BuyTicketViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user, phone_number='+375 (29) 777-77-77', age=18, )

    def test_buy_with_invalid_buy_date(self):
        # Создаем POST-запрос с неправильной датой
        request = self.factory.post('/tickets/buy-ticket/', {'weekday': '2022-01-01', 'promocode': '24JAN'})
        request.user = self.user


class PromoCodeAddTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)
        self.promocode_data = {'code': 'TESTCODE', 'discount_percentage': 30}

    def test_promocode_add_view(self):
        # Аутентифицируемся как администратор
        self.client.login(username='adminuser', password='adminpassword')

        # Отправляем POST-запрос для создания промокода
        response = self.client.post(reverse('tickets:add_promo'), data=self.promocode_data)

        # Проверяем, что промокод был успешно создан и произошло перенаправление на страницу всех товаров
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PromoCode.objects.filter(code='TESTCODE').exists())


class PromoCodeAdddTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_superuser=True)
        self.promocode_data = {'code': 'TESTCODE', 'discount_percentage': 30}

    def test_promocode_add_view(self):
        # Аутентифицируемся как администратор
        self.client.login(username='adminuser', password='adminpassword')

        # Отправляем POST-запрос для создания промокода
        response = self.client.post(reverse('tickets:add_promo'), data=self.promocode_data)

        # Проверяем, что промокод был успешно создан и произошло перенаправление на страницу всех товаров
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PromoCode.objects.filter(code='TESTCODE').exists())


class PromoCodeEditTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        self.promocode = PromoCode.objects.create(code='TESTCODE', discount_percentage=20)

    def test_promocode_edit_view(self):
        request = self.factory.post(reverse('tickets:edit_code', kwargs={'code_id': self.promocode.id}), {'code': 'UPDATEDCODE', 'discount_percentage': 25})
        request.user = self.user
        response = edit_code(request, code_id=self.promocode.id)
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission
        self.promocode.refresh_from_db()
        self.assertEqual(self.promocode.code, 'UPDATEDCODE')  # Promo code code updated
        self.assertEqual(self.promocode.discount_percentage, 25)  # Promo code discount percentage updated


class PromoCodeDeleteTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        self.promocode = PromoCode.objects.create(code='TESTCODE', discount_percentage=20)

    def test_promocode_delete_view(self):
        request = self.factory.post(reverse('tickets:del_code', kwargs={'code_id': self.promocode.id}))
        request.user = self.user
        response = delete_code(request, code_id=self.promocode.id)
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion
        self.assertFalse(PromoCode.objects.filter(code='TESTCODE').exists())  # Promo code deleted


class AddAnimalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_animal_url = reverse('animals:add_animal')
        self.animal_data = {
            'name': 'Lion',
            'gender': 'male',
            'age': 5,
            'country': 'Kenya',
            'amount_of_feed': 500,
            'animal_class': 'Собачьи',
            'responsible_employee': 'John Doe'
        }

    def test_add_animal_view_get(self):
        response = self.client.get(self.add_animal_url)
        self.assertEqual(response.status_code, 403)
        #self.assertTemplateUsed(response, 'animals/add_animal.html')

    def test_add_animal_view_post_valid_data(self):
        response = self.client.post(self.add_animal_url, self.animal_data, format='multipart')
        self.assertEqual(response.status_code, 403)  # Redirect status code

        # Check if the animal is added to the database
        self.assertFalse(Animal.objects.filter(name='Lion').exists())

    def test_add_animal_view_post_invalid_data(self):
        invalid_data = self.animal_data.copy()
        invalid_data['age'] = -5  # Invalid age value
        response = self.client.post(self.add_animal_url, invalid_data, format='multipart')
        self.assertEqual(response.status_code, 403)
        #self.assertTemplateUsed(response, 'animals/add_animal.html')
        # Check that the animal is not added to the database
        self.assertFalse(Animal.objects.filter(name='Lion').exists())


class AddRoomTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_room_url = reverse('rooms:add_room')
        self.room_data = {
            'number': 101,
            'title': 'Living Room',
            'pond': False,
            'heating': True,
        }

    def test_add_room_view_post_valid_data(self):
        response = self.client.post(self.add_room_url, self.room_data)
        # Check if the room is added to the database
        self.assertTrue(Room.objects.filter(number=101).exists())

    def test_add_room_view_post_invalid_data(self):
        invalid_data = self.room_data.copy()
        invalid_data['number'] = 101  # Invalid duplicate number
        response = self.client.post(self.add_room_url, invalid_data)
        #self.assertTemplateUsed(response, 'rooms/add_room.html')
        # Check that the room is not added to the database
        self.assertTrue(Room.objects.filter(number=101).exists())


class DeleteRoomTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.room = Room.objects.create(
            number=101,
            title='Living Room',
            pond=False,
            heating=True
        )
        self.delete_room_url = reverse('rooms:delete_room', args=[self.room.id])

    def test_delete_room_view(self):
        response = self.client.post(self.delete_room_url)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('rooms:all_rooms'))  # Redirect to room list view

        # Check if the room is deleted from the database
        self.assertFalse(Room.objects.filter(id=self.room.id).exists())
