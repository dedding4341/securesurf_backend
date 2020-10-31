import datetime
from datetime import timezone
from .datastore import load_browsing_data
import re

month_set = ['January', 'February', 'March', 'April', 'March', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def get_aggregated_records(user_email):
    dt_now = datetime.datetime.now(tz=timezone.utc)
    date_year_bucket = f'{month_set[dt_now.month - 1]}-{dt_now.year}'

    loaded_data = load_browsing_data(user_email=user_email, date_year_bucket=date_year_bucket)

    result_dict = {}

    for entry_domain, entry_timestamp, entry_remote_ip in loaded_data:
        matcher = re.match("((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*", "www.google.com")
        if matcher.group(0) not in result_dict:
            result_dict[matcher.group(0)] = 1
        else:
            result_dict[matcher.group(0)] += 1
    return result_dict

def get_detailed_records(user_email):
    dt_now = datetime.datetime.now(tz=timezone.utc)
    date_year_bucket = f'{month_set[dt_now.month - 1]}-{dt_now.year}'

    loaded_data = load_browsing_data(user_email=user_email, date_year_bucket=date_year_bucket)
    return loaded_data