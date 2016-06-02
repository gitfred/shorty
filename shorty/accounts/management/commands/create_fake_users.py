import logging

from django.core.management.base import BaseCommand

from accounts.utils import generate_random_users

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create fake users using randomuser.me"

    def add_arguments(self, parser):
        parser.add_argument('users_no', type=int,
                            help="Number of fake users to be generated")

    def handle(self, *args, **options):
        user_no = options.get('users_no')
        try:
            generate_random_users(user_no)
        except Exception as err:
            logger.exception(err)
            self.stderr.write("Error occured: {}".format(err))
        else:
            self.stdout.write(
                "Successfully created {} fake users.".format(user_no))
