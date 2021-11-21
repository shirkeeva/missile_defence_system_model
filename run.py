import time

from mdsm import start_modeling, fill_params, write_logs

if __name__ == '__main__':
    fill_params()
    events: dict[int, str] = start_modeling()
    logs: list[str] = sorted([f'{time.strftime("%H:%M:%S", time.gmtime(item[0]))} {item[1]}'
                              for item in list(events.items())])
    write_logs(logs)
