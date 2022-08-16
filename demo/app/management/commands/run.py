from typing import Any, Optional

from django.core import management


class Command(management.base.BaseCommand):
    help = 'run server at the specified host:port'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        management.call_command('runserver','0.0.0.0:30000')
