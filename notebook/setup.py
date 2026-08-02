import os
import pathlib
import sys

NOTEBOOKS_DIR = pathlib.Path(__file__).parent
REPO_DIR = NOTEBOOKS_DIR.parent

DJANGO_PROJECT_ROOT = REPO_DIR
DJANGO_SETTINGS_MODULE = "config.settings"


def init(verbose=False):
    import django
    from django.apps import apps

    if apps.ready:
        if verbose:
            print("Django already set up — skipping.")
        return

    try:
        import nest_asyncio
        nest_asyncio.apply()
    except ImportError:
        pass

    os.chdir(DJANGO_PROJECT_ROOT)
    sys.path.insert(0, str(DJANGO_PROJECT_ROOT))

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        DJANGO_SETTINGS_MODULE,
    )

    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    django.setup()

    if verbose:
        print(f"Django initialized. Project root: {DJANGO_PROJECT_ROOT}")