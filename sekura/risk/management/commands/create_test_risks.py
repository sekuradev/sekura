from django.core.management.base import BaseCommand
from risk import factories


class Command(BaseCommand):
    help = "Creates Risks with random data"

    def add_arguments(self, parser):
        parser.add_argument("--number", "-n", type=int, default=5, help="Number of risks to create")

    def handle(self, *args, **options):
        for i in range(options["number"]):
            factories.RiskFactory.create()
