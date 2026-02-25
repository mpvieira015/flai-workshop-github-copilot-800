from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
import datetime


class UserAPITestCase(TestCase):
    """Tests for the User API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Test User',
            email='testuser@example.com',
            password='password123',
        )

    def test_list_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data = {'name': 'New User', 'email': 'newuser@example.com', 'password': 'pass'}
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New User')

    def test_get_user(self):
        response = self.client.get(f'/api/users/{self.user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_update_user(self):
        data = {'name': 'Updated User', 'email': 'testuser@example.com', 'password': 'newpass'}
        response = self.client.put(f'/api/users/{self.user.pk}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated User')

    def test_delete_user(self):
        response = self.client.delete(f'/api/users/{self.user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TeamAPITestCase(TestCase):
    """Tests for the Team API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Team Alpha', members=[])

    def test_list_teams(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team(self):
        data = {'name': 'Team Beta', 'members': []}
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Team Beta')

    def test_get_team(self):
        response = self.client.get(f'/api/teams/{self.team.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Team Alpha')

    def test_delete_team(self):
        response = self.client.delete(f'/api/teams/{self.team.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ActivityAPITestCase(TestCase):
    """Tests for the Activity API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.activity = Activity.objects.create(
            user='testuser',
            activity_type='Running',
            duration=30.0,
            date=datetime.date.today(),
        )

    def test_list_activities(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_activity(self):
        data = {
            'user': 'anotheruser',
            'activity_type': 'Cycling',
            'duration': 45.0,
            'date': str(datetime.date.today()),
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['activity_type'], 'Cycling')

    def test_get_activity(self):
        response = self.client.get(f'/api/activities/{self.activity.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activity_type'], 'Running')

    def test_delete_activity(self):
        response = self.client.delete(f'/api/activities/{self.activity.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LeaderboardAPITestCase(TestCase):
    """Tests for the Leaderboard API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.entry = Leaderboard.objects.create(user='topuser', score=1000)

    def test_list_leaderboard(self):
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_leaderboard_entry(self):
        data = {'user': 'newuser', 'score': 500}
        response = self.client.post('/api/leaderboard/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], 500)

    def test_get_leaderboard_entry(self):
        response = self.client.get(f'/api/leaderboard/{self.entry.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], 'topuser')

    def test_delete_leaderboard_entry(self):
        response = self.client.delete(f'/api/leaderboard/{self.entry.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class WorkoutAPITestCase(TestCase):
    """Tests for the Workout API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='Morning Run',
            description='A refreshing morning run',
            duration=30.0,
        )

    def test_list_workouts(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_workout(self):
        data = {'name': 'Evening Yoga', 'description': 'Relaxing yoga session', 'duration': 60.0}
        response = self.client.post('/api/workouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Evening Yoga')

    def test_get_workout(self):
        response = self.client.get(f'/api/workouts/{self.workout.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Morning Run')

    def test_delete_workout(self):
        response = self.client.delete(f'/api/workouts/{self.workout.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIRootTestCase(TestCase):
    """Tests for the API root endpoint."""

    def setUp(self):
        self.client = APIClient()

    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

    def test_root_redirects_to_api(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
