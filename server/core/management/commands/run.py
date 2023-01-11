from typing import Any, Optional

from django.core import management
from server.settings import env


class Command(management.base.BaseCommand):
    help = 'run server at the specified host:port'

    def add_arguments(self, parser) -> None:
        parser.add_argument('dev')

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if options['dev']:
            print(env.__dict__)
            management.call_command('runserver',f"0.0.0.0:{env.str('PORT')}")
