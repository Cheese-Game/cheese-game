import time


def log(msg) -> None:
    current_time: time.struct_time = time.localtime(time.time())

    hrs: str = pad(str(current_time.tm_hour))
    mins: str = pad(str(current_time.tm_min))
    secs: str = pad(str(current_time.tm_sec))

    print(f'[{hrs}:{mins}:{secs}] {msg}')


def pad(string) -> str:
    while len(string) < 2:
        string = '0' + string
    return string
