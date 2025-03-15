from flask import Blueprint
from datetime import datetime
import base64

filBp = Blueprint("filter", __name__)


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
