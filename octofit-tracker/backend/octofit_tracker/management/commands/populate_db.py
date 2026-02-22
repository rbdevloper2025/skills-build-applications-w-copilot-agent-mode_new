from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Team Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='Team DC Superheroes')

        # Create users
        users = [
            User(name='Spider-Man', email='spiderman@marvel.com', team=marvel, is_superhero=True),
            User(name='Iron Man', email='ironman@marvel.com', team=marvel, is_superhero=True),
            User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc, is_superhero=True),
            User(name='Batman', email='batman@dc.com', team=dc, is_superhero=True),
        ]
        User.objects.bulk_create(users)

        # Refresh users from DB to get IDs
        users = list(User.objects.all())

        # Create workouts
        workouts = [
            Workout(name='Strength Training', description='Full body workout'),
            Workout(name='Cardio Blast', description='High intensity cardio'),
        ]
        Workout.objects.bulk_create(workouts)
        for workout in Workout.objects.all():
            workout.suggested_for.set(users)

        # Create activities
        Activity.objects.create(user=users[0], type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], type='Yoga', duration=40, date=timezone.now().date())

        # Create leaderboard entries
        Leaderboard.objects.create(team=marvel, user=users[0], score=100)
        Leaderboard.objects.create(team=marvel, user=users[1], score=90)
        Leaderboard.objects.create(team=dc, user=users[2], score=110)
        Leaderboard.objects.create(team=dc, user=users[3], score=95)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
