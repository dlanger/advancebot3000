# Put settings here, so that they can be overridden by non-VC'ed values in local_settings.py

SENTRY_DSN = None
POSSIBLE_EMAIL_RECIPIENTS = ()

try:
    from local_settings import *
except:
    pass