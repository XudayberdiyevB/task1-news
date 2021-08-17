import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from .serializers import NewsCategorySerializer, NewsSerializer
from .models import NewsCategoryModel, NewsModel

client = Client()

# test for NewsCategoryModel
class NewsCategoryModelTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

    def test_category_name(self):
        categ_sport = NewsCategoryModel.objects.get(name="Sport yangiliklari")
        categ_world = NewsCategoryModel.objects.get(name="Dunyo yangiliklari")
        categ_uzb = NewsCategoryModel.objects.get(name="O'zbekiston yangiliklari")

        self.assertEqual(categ_sport.name, "Sport yangiliklari")
        self.assertEqual(categ_world.name, "Dunyo yangiliklari")
        self.assertEqual(categ_uzb.name, "O'zbekiston yangiliklari")


# test for NewsCategory get
class GetAllNewsCategoryTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

    def test_get_all_categories(self):
        response = self.client.get(reverse('categories'))
        categories = NewsCategoryModel.objects.all()
        serializer = NewsCategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# test for NewsCategory create, post
class CreateNewsCategoryTest(TestCase):
    def setUp(self):
        self.valid_category = {
            'name': 'oxirgi yangiliklar'
        }
        self.invalid_category = {
            'name': ''
        }

    def test_create_valid_category(self):
        response = client.post(reverse('categories'), data=json.dumps(self.valid_category),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_category(self):
        response = client.post(reverse('categories'), data=json.dumps(self.invalid_category),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# test for NewsCategory get single
class GetSigleNewsCategoryTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

    def test_get_valid_single_category(self):
        response = client.get(reverse('category_detail', kwargs={'pk': self.categ_sport.pk}))
        category = NewsCategoryModel.objects.get(pk=self.categ_sport.pk)
        serializer = NewsCategorySerializer(category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_category(self):
        response = client.get(reverse('category_detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# test for NewsCategory update, put
class UpdateSingleNewsCategoryTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

        self.valid_category = {
            'name': 'oxirgi yangiliklar'
        }
        self.invalid_category = {
            'name': ''
        }

    def test_update_valid_category(self):
        response = client.put(reverse('category_detail', kwargs={'pk': self.categ_world.pk}),
                              data=json.dumps(self.valid_category), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_category(self):
        response = client.put(reverse('category_detail', kwargs={'pk': self.categ_world.pk}),
                              data=json.dumps(self.invalid_category), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# test for NewsCategory delete
class DeleteSingleNewsCategoryTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

    def test_delete_valid_category(self):
        response = client.delete(reverse('category_detail', kwargs={'pk': self.categ_uzb.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_category(self):
        response = client.delete(reverse('category_detail', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# test for NewsModel
class NewsModelTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

        self.news1 = NewsModel.objects.create(title="O‘zbekiston milliy jamoasining yangi bosh murabbiyi e'lon qilindi",
                                              content="Sloveniyalik taniqli mutaxassis, Iroq milliy jamoasining sobiq bosh murabbiyi Srechko Katanets O‘zbekiston milliy jamoasi bosh murabbiyi etib tayinlanadi.",
                                              created_date='2021-08-13T12:13:01.419163Z',
                                              count_of_viewed=100,
                                              news_category=self.categ_uzb,
                                              )
        self.news2 = NewsModel.objects.create(title="AQSh, Britaniya va Kanada Afg‘onistonga minglab askar jo‘natmoqda",
                                              content="Pentagon matbuot kotibi Jon Kirbining ta'kidlashicha, AQShning Kobuldagi elchixonasi xodimlarini xavfsiz evakuatsiya qilish uchun Afg‘onistonga yaqin 48 soat ichida 3 ta batalon, ya'ni 3 mingga yaqin harbiy jo‘natiladi.",
                                              created_date='2021-08-14T05:23:00.928723Z',
                                              count_of_viewed=150,
                                              news_category=self.categ_world,
                                              )

    def test_news_title(self):
        news1 = NewsModel.objects.get(title="O‘zbekiston milliy jamoasining yangi bosh murabbiyi e'lon qilindi")
        news2 = NewsModel.objects.get(title="AQSh, Britaniya va Kanada Afg‘onistonga minglab askar jo‘natmoqda")

        self.assertEqual(news1.title, "O‘zbekiston milliy jamoasining yangi bosh murabbiyi e'lon qilindi")
        self.assertEqual(news2.title, "AQSh, Britaniya va Kanada Afg‘onistonga minglab askar jo‘natmoqda")


# test for News get
class GetAllNewsTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

        self.news1 = NewsModel.objects.create(title="O‘zbekiston milliy jamoasining yangi bosh murabbiyi e'lon qilindi",
                                              content="Sloveniyalik taniqli mutaxassis, Iroq milliy jamoasining sobiq bosh murabbiyi Srechko Katanets O‘zbekiston milliy jamoasi bosh murabbiyi etib tayinlanadi.",
                                              created_date='2021-08-13T12:13:01.419163Z',
                                              count_of_viewed=100,
                                              news_category=self.categ_uzb,
                                              )
        self.news2 = NewsModel.objects.create(title="AQSh, Britaniya va Kanada Afg‘onistonga minglab askar jo‘natmoqda",
                                              content="Pentagon matbuot kotibi Jon Kirbining ta'kidlashicha, AQShning Kobuldagi elchixonasi xodimlarini xavfsiz evakuatsiya qilish uchun Afg‘onistonga yaqin 48 soat ichida 3 ta batalon, ya'ni 3 mingga yaqin harbiy jo‘natiladi.",
                                              created_date='2021-08-14T05:23:00.928723Z',
                                              count_of_viewed=150,
                                              news_category=self.categ_world,
                                              )

    def test_get_all_news(self):
        response = client.get(reverse('news'))
        news = NewsModel.objects.all()
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# test for News create, post
class CreateNewsTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

        self.valid_news = NewsModel.objects.create(
            title="O‘zbekiston milliy jamoasining yangi bosh murabbiyi e'lon qilindi",
            content="Sloveniyalik taniqli mutaxassis, Iroq milliy jamoasining sobiq bosh murabbiyi Srechko Katanets O‘zbekiston milliy jamoasi bosh murabbiyi etib tayinlanadi.",
            created_date='2021-08-13T12:13:01.419163Z',
            count_of_viewed=100,
            news_category=self.categ_uzb
        )
        self.invalid_news = NewsModel.objects.create(
            title="AQSh, Britaniya va Kanada Afg‘onistonga minglab askar jo‘natmoqda",
            content="",
            created_date='2021-08-14T05:23:00.928723Z',
            count_of_viewed=150,
            news_category=self.categ_world
        )

    def test_create_valid_news(self):
        serializer = NewsSerializer(self.valid_news)
        response = client.post(reverse("news"), data=serializer.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_news(self):
        serializer = NewsSerializer(self.invalid_news)
        response = client.post(reverse("news"), data=serializer.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# test for News get single
class GetSingleNewsTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

        self.news1 = NewsModel.objects.create(title="O‘zbekiston milliy jamoasining yangi bosh murabbiyi e'lon qilindi",
                                              content="Sloveniyalik taniqli mutaxassis, Iroq milliy jamoasining sobiq bosh murabbiyi Srechko Katanets O‘zbekiston milliy jamoasi bosh murabbiyi etib tayinlanadi.",
                                              created_date='2021-08-13T12:13:01.419163Z',
                                              count_of_viewed=100,
                                              news_category=self.categ_uzb,
                                              )
        self.news2 = NewsModel.objects.create(title="AQSh, Britaniya va Kanada Afg‘onistonga minglab askar jo‘natmoqda",
                                              content="Pentagon matbuot kotibi Jon Kirbining ta'kidlashicha, AQShning Kobuldagi elchixonasi xodimlarini xavfsiz evakuatsiya qilish uchun Afg‘onistonga yaqin 48 soat ichida 3 ta batalon, ya'ni 3 mingga yaqin harbiy jo‘natiladi.",
                                              created_date='2021-08-14T05:23:00.928723Z',
                                              count_of_viewed=150,
                                              news_category=self.categ_world,
                                              )

    def test_get_single_valid_news(self):
        response = client.get(reverse("news_detail", kwargs={'pk': self.news1.pk}))
        news = NewsModel.objects.get(pk=self.news1.pk)
        serializer = NewsSerializer(news)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_invalid_news(self):
        response = client.get(reverse("news_detail", kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# test for News update, put
class UpdateSingleNewsTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

        self.valid_news = NewsModel.objects.create(
            title="O‘zbekiston milliy jamoasining yangi bosh murabbiyi e'lon qilindi",
            content="Sloveniyalik taniqli mutaxassis, Iroq milliy jamoasining sobiq bosh murabbiyi Srechko Katanets O‘zbekiston milliy jamoasi bosh murabbiyi etib tayinlanadi.",
            created_date='2021-08-13T12:13:01.419163Z',
            count_of_viewed=100,
            news_category=self.categ_uzb,
        )
        self.invalid_news = NewsModel.objects.create(
            title="O‘zbekiston milliy jamoasining yangi bosh murabbiyi e'lon qilindi",
            content="",
            created_date='2021-08-13T12:13:01.419163Z',
            count_of_viewed=100,
            news_category=self.categ_uzb,
        )

    def test_update_valid_news(self):
        serializer = NewsSerializer(self.valid_news)
        response = client.put(reverse("news_detail", kwargs={'pk': self.valid_news.pk}),
                              data=serializer.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_news(self):
        serializer = NewsSerializer(self.invalid_news)
        response = client.put(reverse("news_detail", kwargs={'pk': self.invalid_news.pk}),
                              data=serializer.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleNewsTest(TestCase):
    def setUp(self):
        self.categ_sport = NewsCategoryModel.objects.create(name="Sport yangiliklari")
        self.categ_world = NewsCategoryModel.objects.create(name="Dunyo yangiliklari")
        self.categ_uzb = NewsCategoryModel.objects.create(name="O'zbekiston yangiliklari")

        self.news = NewsModel.objects.create(
            title="O‘zbekiston milliy jamoasining yangi bosh murabbiyi e'lon qilindi",
            content="Sloveniyalik taniqli mutaxassis, Iroq milliy jamoasining sobiq bosh murabbiyi Srechko Katanets O‘zbekiston milliy jamoasi bosh murabbiyi etib tayinlanadi.",
            created_date='2021-08-13T12:13:01.419163Z',
            count_of_viewed=100,
            news_category=self.categ_uzb,
        )

    def test_delete_valid_news(self):
        response = client.delete(reverse('category_detail', kwargs={'pk': self.news.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_news(self):
        response = client.delete(reverse('category_detail', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

