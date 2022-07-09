from ezaws.utils.timing import (
    epoch_ms_to_date_time,
    convert_to_local,
    current_ms_after_epoch,
    datetime_to_epoch_in_ms,
    epoch_seconds_ago,
    epoch_minutes_ago,
    epoch_hours_ago,
    epoch_days_ago,
    date_seconds_ago,
    date_minutes_ago,
    date_days_ago,
    epoch_ms_to_date_time,
    epoch_to_date_time,
    convert_to_local,
)

import datetime


def test_current_ms_after_epoch():
    ms_after_epoch = current_ms_after_epoch()
    assert isinstance(ms_after_epoch, int)


def test_epoch_ms_to_date_time():
    date_time = epoch_ms_to_date_time(1)
    assert isinstance(date_time, datetime.datetime)


def test_datetime_to_epoch_in_ms():
    datetime_to_epoch_in_ms_result = datetime_to_epoch_in_ms(datetime.datetime.now())
    assert isinstance(datetime_to_epoch_in_ms_result, int)


def test_convert_to_local():
    date_time = convert_to_local(datetime.datetime.now())
    assert isinstance(date_time, datetime.datetime)


def test_epoch_to_date_time():
    epoch_to_date_time_return = epoch_to_date_time(1.1)
    assert isinstance(epoch_to_date_time_return, datetime.datetime)


def test_xxx_ago():
    test_func = [
        epoch_seconds_ago,
        epoch_minutes_ago,
        epoch_hours_ago,
        epoch_days_ago,
        date_seconds_ago,
        date_minutes_ago,
        date_days_ago,
    ]
    for f in test_func:
        assert isinstance(f(1), int)
