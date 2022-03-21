import time
import datetime
from typing import Callable, Optional
from dateutil import tz


def current_ms_after_epoch() -> int:
    """Returns the current epoch in ms."""
    ms = int(time.time() * 1000)
    return ms


def datetime_to_epoch_in_ms(date: datetime.datetime) -> int:
    """Converts given datetime.datetime instance to epoch in ms."""
    seconds = date.timestamp()
    return int(seconds * 1000)


def epoch_seconds_ago(n: int) -> Callable[[datetime.datetime], int]:
    """Returns the epoch in ms as it was exactly n-seconds ago."""
    date_time = datetime.datetime.now() - datetime.timedelta(seconds=n)
    return datetime_to_epoch_in_ms(date_time)


def epoch_minutes_ago(n: int) -> Callable[[datetime.datetime], int]:
    """Returns the epoch in ms as it was exactly n-minutes ago."""
    date_time = datetime.datetime.now() - datetime.timedelta(minutes=n)
    return datetime_to_epoch_in_ms(date_time)


def epoch_hours_ago(n: int) -> Callable[[datetime.datetime], int]:
    """Returns the epoch in ms as it was exactly n-hours ago."""
    date_time = datetime.datetime.now() - datetime.timedelta(hours=n)
    return datetime_to_epoch_in_ms(date_time)


def epoch_days_ago(n: int) -> Callable[[datetime.datetime], int]:
    """Returns the epoch in ms as it was exactly n-days ago."""
    date_time = datetime.datetime.now() - datetime.timedelta(days=n)
    return datetime_to_epoch_in_ms(date_time)


def date_seconds_ago(n: int) -> datetime.datetime:
    """Returns the epoch in ms as it was exactly n-seconds ago."""
    date_time = datetime.datetime.now() - datetime.timedelta(minutes=n)
    return datetime_to_epoch_in_ms(date_time)


def date_minutes_ago(n: int) -> datetime.datetime:
    """Returns the epoch in ms as it was exactly n-minutes ago."""
    date_time = datetime.datetime.now() - datetime.timedelta(minutes=n)
    return datetime_to_epoch_in_ms(date_time)


def date_days_ago(n: int) -> datetime.datetime:
    """Returns the epoch in ms as it was exactly n-days ago."""
    date_time = datetime.datetime.now() - datetime.timedelta(days=n)
    return datetime_to_epoch_in_ms(date_time)


def epoch_ms_to_date_time(epoch_in_ms: int) -> datetime.datetime:
    """Take the number of milliseconds since epoch and return a datetime object"""
    epoch_time = epoch_in_ms / 1000.0
    return datetime.datetime.fromtimestamp(epoch_time)


def epoch_to_date_time(epoch_time: float) -> datetime.datetime:
    """Take the number of milliseconds since epoch and return a datetime object"""
    return datetime.datetime.fromtimestamp(epoch_time)


def convert_to_local(date: datetime.datetime, local_zone: Optional[str] = None):
    """Convert UTC to a local date. If no local date is give, 'tz.tzlocal()' is used."""
    to_zone = local_zone if local_zone else tz.tzlocal()
    # date = date.replace(tzinfo=from_zone)
    converted = date.astimezone(to_zone)
    return converted


"""
def time_to_epoch_in_ms(
    year: int,
    month: int,
    day: int,
    hour: Optional[int],
    minute: Optional[int],
    second: Optional[int],
    microsecond: Optional[int],
    tzinfo: Optional[Union[None, datetime.tzinfo]],
) -> int:

    dttm = datetime.datetime(
        year, month, day, hour, minute, second, microsecond, tzinfo
    )
    print(dttm)
    pass
"""


if __name__ == "__main__":
    now = current_ms_after_epoch()
    print(now)

    # epoch = datetime_to_epoc_in_ms(date=datetime.datetime(2022, 3, 19, 11, 35, 0, 0))
    # print(epoch)
    # epoch = datetime_to_epoc_in_ms(date=datetime.datetime(2022, 3, 19, 11, 35))
    # print(epoch)
    one = epoch_minutes_ago(1)
    two = epoch_minutes_ago(2)
    five = epoch_minutes_ago(5)
    ten = epoch_minutes_ago(10)
    print(now, now / 1000)
    print(one, one / 1000)
    print(two, two / 1000)
    print(five, five / 1000)
    print(ten, ten / 1000)
