import datetime

def log(obj, *, src="CCC-Backend"):
    time = datetime.datetime.now()
    print(f"[{time}]{src}: {obj}")