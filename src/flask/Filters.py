from flask import Blueprint
from datetime import datetime, timedelta
import base64
import pytz

filBp = Blueprint("filter", __name__)
LOCAL_TZ = pytz.timezone("America/Toronto")


@filBp.app_template_filter('strftime')
def strftime_filter(value, fmt='%Y-%m-%d'):
    if value:
        if value == "Birthday empty":
            return value
        try:
            original_date_format = "%a, %d %b %Y %H:%M:%S %Z"
            datetime_obj = datetime.strptime(value, original_date_format)

            formatted_date_str = datetime_obj.strftime(fmt)
            return formatted_date_str
        except ValueError:
            return value
    return "Birthday empty"


@filBp.app_template_filter('timeago')
def time_ago(value):
    if not value:
        return "Unknown"

    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        value = pytz.utc.localize(value)  # set as utc time

    # convert to local time
    local_time = value.astimezone(LOCAL_TZ)

    now = datetime.now(LOCAL_TZ)  # now local time
    delta = now - local_time

    if delta < timedelta(minutes=1):
        return f"{int(delta.total_seconds())} secs ago"
    elif delta < timedelta(hours=1):
        return f"{int(delta.total_seconds() // 60)} mins ago"
    elif delta < timedelta(days=1):
        return f"{int(delta.total_seconds() // 3600)} hours ago"
    else:
        return value.strftime("%Y-%m-%d")
