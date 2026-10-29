from django.test import TestCase
from django.urls import reverse
from django.db import connection
from .models import Human, Goalkeeper, FieldPlayer, Player


class PlayerTests(TestCase):
    def setUp(self):
        self.data = {'id':'12345', 'name':'Ananth', 'player_type':'Goalie',
                     'count':10, 'score':30}

    def test_python_inheritance_and_zero_matches(self):
        goalkeeper = Goalkeeper('Keeper',12345,0,0)
        fieldplayer = FieldPlayer('Scorer',23456,10,8)
        self.assertIsInstance(goalkeeper, Human)
        self.assertIsInstance(fieldplayer, Human)
        self.assertEqual(goalkeeper.stoprate, 0)
        self.assertEqual(fieldplayer.GoalCount, 8)

    def test_one_player_table(self):
        tables = []
        for table in connection.introspection.table_names():
            if table.startswith('myapp_'):
                tables.append(table)
        self.assertEqual(tables, ['myapp_player'])

    def test_pages_open(self):
        for name in ['start','register','display','findbest','searchplayer']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_insert_both_types(self):
        response = self.client.post(reverse('register'), self.data)
        self.assertContains(response, 'Successfully inserted')
        self.assertContains(response, '>OK</button>')
        goalkeeper = Player.objects.get(id=12345)
        self.assertEqual(goalkeeper.TotalStoppingShots, 30)
        self.assertEqual(goalkeeper.GoalCount, 0)
        self.assertEqual(goalkeeper.stoprate(), 3)
        response = self.client.post(reverse('register'), {
            **self.data, 'id':'23456', 'player_type':'Field Player', 'score':8,
        })
        self.assertContains(response, 'Successfully inserted')
        fieldplayer = Player.objects.get(id=23456)
        self.assertEqual(fieldplayer.GoalCount, 8)
        self.assertEqual(fieldplayer.TotalStoppingShots, 0)

    def test_invalid_and_duplicate_ids_show_separate_message(self):
        for idx in ['', '1234', '123456', '01234', 'abcde', '１２３４５']:
            response = self.client.post(reverse('register'), {**self.data,'id':idx})
            self.assertContains(response, 'Invalid PlayerID')
            self.assertTemplateUsed(response, 'message.html')
            self.assertContains(response, '>OK</button>')
        self.assertEqual(Player.objects.count(), 0)
        self.client.post(reverse('register'), self.data)
        response = self.client.post(reverse('register'), {
            **self.data, 'player_type':'Field Player',
        })
        self.assertContains(response, 'Invalid PlayerID')
        self.assertEqual(Player.objects.count(), 1)

    def test_invalid_other_fields_keep_errors_and_do_not_save(self):
        for changes in [{'count':-1}, {'score':-3}, {'player_type':'Bowler'}, {'name':''}]:
            response = self.client.post(reverse('register'), {**self.data, **changes})
            self.assertTemplateUsed(response, 'register.html')
            self.assertTrue(response.context['form'].errors)
        self.assertEqual(Player.objects.count(), 0)

    def test_search_found_and_missing(self):
        self.client.post(reverse('register'), self.data)
        response = self.client.post(reverse('searchplayer'), {'id':'12345'})
        self.assertContains(response, 'Ananth')
        self.assertContains(response, 'Goalie')
        for idx in ['99999', 'abc', '', '１２３４５']:
            response = self.client.post(reverse('searchplayer'), {'id':idx})
            self.assertContains(response, 'PlayerID Not Matched')
            self.assertTemplateUsed(response, 'message.html')
            self.assertContains(response, '>OK</button>')

    def test_best_goalie_uses_rate_not_total_shots(self):
        Player.objects.create(id=11111, name='Many shots', player_type='Goalie',
                              count=20, TotalStoppingShots=50)
        winner = Player.objects.create(id=22222, name='Higher rate', player_type='Goalie',
                                       count=5, TotalStoppingShots=20)
        Player.objects.create(id=33333, name='No matches', player_type='Goalie', count=0)
        response = self.client.post(reverse('findbest'), {'player_type':'Goalie'})
        self.assertEqual(response.context['best'], winner)
        self.assertContains(response, '4.00')

    def test_best_field_player_and_empty_type(self):
        response = self.client.post(reverse('findbest'), {'player_type':'Field Player'})
        self.assertContains(response, 'No players found for this type.')
        Player.objects.create(id=11111, name='Fewer goals', player_type='Field Player',
                              count=1, GoalCount=5)
        winner = Player.objects.create(id=22222, name='More goals', player_type='Field Player',
                                       count=20, GoalCount=10)
        response = self.client.post(reverse('findbest'), {'player_type':'Field Player'})
        self.assertEqual(response.context['best'], winner)

    def test_display_has_both_types(self):
        Player.objects.create(id=11111, name='Keeper', player_type='Goalie',
                              count=5, TotalStoppingShots=10)
        Player.objects.create(id=22222, name='Scorer', player_type='Field Player',
                              count=5, GoalCount=8)
        response = self.client.get(reverse('display'))
        self.assertContains(response, 'Keeper')
        self.assertContains(response, 'Scorer')
        self.assertContains(response, '2.00')
