from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write('Creating users (superheroes)...')
        users_data = [
            {'name': 'Tony Stark', 'email': 'ironman@marvel.com', 'password': 'ironman123'},
            {'name': 'Steve Rogers', 'email': 'captain@marvel.com', 'password': 'captain123'},
            {'name': 'Natasha Romanoff', 'email': 'blackwidow@marvel.com', 'password': 'widow123'},
            {'name': 'Bruce Banner', 'email': 'hulk@marvel.com', 'password': 'hulk123'},
            {'name': 'Thor Odinson', 'email': 'thor@marvel.com', 'password': 'thor123'},
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com', 'password': 'batman123'},
            {'name': 'Clark Kent', 'email': 'superman@dc.com', 'password': 'superman123'},
            {'name': 'Diana Prince', 'email': 'wonderwoman@dc.com', 'password': 'wonder123'},
            {'name': 'Barry Allen', 'email': 'flash@dc.com', 'password': 'flash123'},
            {'name': 'Hal Jordan', 'email': 'greenlantern@dc.com', 'password': 'lantern123'},
        ]
        users = {}
        for u in users_data:
            user, created = User.objects.get_or_create(email=u['email'], defaults={'name': u['name'], 'password': u['password']})
            users[u['name']] = user
            if created:
                self.stdout.write(f"  Created user: {user.name}")
            else:
                self.stdout.write(f"  Found existing user: {user.name}")

        self.stdout.write('Creating teams...')
        marvel_members = [users['Tony Stark'].pk, users['Steve Rogers'].pk,
                          users['Natasha Romanoff'].pk, users['Bruce Banner'].pk, users['Thor Odinson'].pk]
        dc_members = [users['Bruce Wayne'].pk, users['Clark Kent'].pk,
                      users['Diana Prince'].pk, users['Barry Allen'].pk, users['Hal Jordan'].pk]

        team_marvel, _ = Team.objects.get_or_create(name='Team Marvel', defaults={'members': [str(pk) for pk in marvel_members]})
        team_dc, _ = Team.objects.get_or_create(name='Team DC', defaults={'members': [str(pk) for pk in dc_members]})
        self.stdout.write(f"  Created team: {team_marvel.name}")
        self.stdout.write(f"  Created team: {team_dc.name}")

        self.stdout.write('Creating activities...')
        activities_data = [
            {'user': 'Tony Stark', 'activity_type': 'Running', 'duration': 30.0, 'date': date(2024, 1, 10)},
            {'user': 'Steve Rogers', 'activity_type': 'Cycling', 'duration': 45.0, 'date': date(2024, 1, 11)},
            {'user': 'Natasha Romanoff', 'activity_type': 'Yoga', 'duration': 60.0, 'date': date(2024, 1, 12)},
            {'user': 'Bruce Banner', 'activity_type': 'Swimming', 'duration': 40.0, 'date': date(2024, 1, 13)},
            {'user': 'Thor Odinson', 'activity_type': 'Weightlifting', 'duration': 50.0, 'date': date(2024, 1, 14)},
            {'user': 'Bruce Wayne', 'activity_type': 'Martial Arts', 'duration': 90.0, 'date': date(2024, 1, 10)},
            {'user': 'Clark Kent', 'activity_type': 'Running', 'duration': 20.0, 'date': date(2024, 1, 11)},
            {'user': 'Diana Prince', 'activity_type': 'Archery', 'duration': 35.0, 'date': date(2024, 1, 12)},
            {'user': 'Barry Allen', 'activity_type': 'Sprinting', 'duration': 15.0, 'date': date(2024, 1, 13)},
            {'user': 'Hal Jordan', 'activity_type': 'Flying Simulation', 'duration': 55.0, 'date': date(2024, 1, 14)},
        ]
        for a in activities_data:
            activity = Activity.objects.create(**a)
            self.stdout.write(f"  Created activity: {activity.user} - {activity.activity_type}")

        self.stdout.write('Creating leaderboard entries...')
        leaderboard_data = [
            {'user': 'Tony Stark', 'score': 1500},
            {'user': 'Steve Rogers', 'score': 1800},
            {'user': 'Natasha Romanoff', 'score': 1600},
            {'user': 'Bruce Banner', 'score': 1200},
            {'user': 'Thor Odinson', 'score': 2000},
            {'user': 'Bruce Wayne', 'score': 1900},
            {'user': 'Clark Kent', 'score': 2100},
            {'user': 'Diana Prince', 'score': 1700},
            {'user': 'Barry Allen', 'score': 2200},
            {'user': 'Hal Jordan', 'score': 1400},
        ]
        for l in leaderboard_data:
            entry = Leaderboard.objects.create(**l)
            self.stdout.write(f"  Created leaderboard entry: {entry.user} - {entry.score}")

        self.stdout.write('Creating workouts...')
        workouts_data = [
            {'name': 'Iron Man Endurance', 'description': 'High-intensity cardio and strength training inspired by Tony Stark.', 'duration': 60.0},
            {'name': 'Captain America Bootcamp', 'description': 'Military-style workout with running, push-ups, and obstacle courses.', 'duration': 75.0},
            {'name': 'Black Widow Stealth Training', 'description': 'Agility, flexibility, and martial arts conditioning.', 'duration': 50.0},
            {'name': 'Hulk Smash Strength', 'description': 'Maximum weight lifting and power exercises.', 'duration': 45.0},
            {'name': 'Thor Thunder Circuit', 'description': 'Full body strength and conditioning circuit inspired by the Asgardian.', 'duration': 55.0},
            {'name': 'Batman Dark Knight Workout', 'description': 'Martial arts, gymnastics, and stealth training.', 'duration': 90.0},
            {'name': 'Superman Kryptonian Fitness', 'description': 'Super strength and flight simulation training.', 'duration': 40.0},
            {'name': 'Wonder Woman Amazon Training', 'description': 'Warrior fitness with weapons training and endurance.', 'duration': 65.0},
            {'name': 'Flash Speed Training', 'description': 'Sprint intervals and fast-twitch muscle activation.', 'duration': 30.0},
            {'name': 'Green Lantern Willpower Circuit', 'description': 'Mental and physical endurance training.', 'duration': 50.0},
        ]
        for w in workouts_data:
            workout = Workout.objects.create(**w)
            self.stdout.write(f"  Created workout: {workout.name}")

        self.stdout.write(self.style.SUCCESS('Successfully populated the octofit_db database with test data!'))
