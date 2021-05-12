from django.core.management import BaseCommand, CommandParser

from endpoints.models import UniqueEndpoints
from endpoints.utils import get_random_string

from django.conf import settings


class Command(BaseCommand):
    help = "Insert unique endpoint names into db"

    def add_arguments(self, parser: CommandParser) -> None:
        """
        :param parser:
        :return:
        """
        parser.add_argument(
            "--count", type=int, help="Number of endpoint names to be generated"
        )

    def handle(self, *args, **options):
        """
        :param args:
        :param options:
        :return:
        """
        endpoint_names_count = options.get("count")
        if endpoint_names_count is None:
            endpoint_names_count = settings.DEFAULT_ENDPOINT_INSERTION_COUNT
        while endpoint_names_count > 0:
            try:
                UniqueEndpoints.objects.create(name=get_random_string())
            except Exception:
                pass
            else:
                endpoint_names_count -= 1
        self.stdout.write(
            self.style.SUCCESS(f"SUCCESS - Inserted many unique endpoint names in db.")
        )
