#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horseshow.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc: #pragma: no cover
        raise ImportError( #pragma: no cover
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
