from .token_services import TokenServices

from datetime import datetime, timedelta


def test_get_refresh_after_long_token():
    """
    The now calculated in the function is going to be different to the now
    generated in the test so just make sure that they're < 1 second apart.
    """
    now = datetime.now()
    now_plus_30 = now + timedelta(days=30)
    refresh_after = TokenServices.get_refresh_after(now_plus_30)
    now_plus_6 = now + timedelta(days=6)
    assert abs(now_plus_6 - refresh_after) < timedelta(seconds=1)


def test_get_refresh_after_short_token():
    now = datetime.now()
    now_plus_5 = now + timedelta(days=5)
    refresh_after = TokenServices.get_refresh_after(now_plus_5)
    now_plus_3 = now + timedelta(days=3)
    assert abs(now_plus_3 - refresh_after) < timedelta(seconds=1)


def test_get_refresh_after_very_short_token():
    now = datetime.now()
    now_plus_1 = now + timedelta(days=1)
    refresh_after = TokenServices.get_refresh_after(now_plus_1)
    now_minus_1 = now - timedelta(days=1)
    assert abs(now_minus_1 - refresh_after) < timedelta(seconds=1)
