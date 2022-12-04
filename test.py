from datetime import datetime, timedelta, timezone
from jwt.utils import get_int_from_datetime

date = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'

print(date)