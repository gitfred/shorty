from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create fake users using randomuser.me"

    def add_arguments(self, parser):
        parser.add_arguments('users_no', type=int,
                             help="Number of fake users to be generated")

    def handle(self, *args, **options):
        user_no = options.get('users_no')

