#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_root.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if os.environ.get("REMOTE_DEBUGGER", 0) == '1':
        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
            try:
                import ptvsd
                print('\nConnecting remote debugger ...')
                ptvsd.enable_attach(address=("0.0.0.0", 5678))
            except Exception:
                raise Exception("Something went wrong - Could not attach the remote debugger")
            print("Attached remote debugger on http://0.0.0.0:5678/\n")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
