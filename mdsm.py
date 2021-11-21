from typing import Optional

from matplotlib import pyplot as plt
import numpy as np

from events import Events

MEAN_MISSILE_FREQUENCY: Optional[int] = None
MEAN_ANTI_MISSILE_SPEED: Optional[int] = None
VARIANCE_ANTI_MISSILE_SPEED: Optional[int] = None
COUNT_OF_MISSILES: Optional[int] = None
NUMBER_OF_ANTI_MISSILES: Optional[int] = None
DETECTION_DISTANCE: Optional[int] = None
MEAN_TO_RELOAD: Optional[int] = None
STANDART_DEVIATION_TO_RELOAD: Optional[int] = None
MISSILE_SPEED_KM_PER_HOUR: Optional[int] = None
missile_speed: Optional[float] = None
time_to_hit: Optional[int] = None


def fill_params() -> None:
    """
        MEAN_MISSILE_FREQUENCY: Final[int] = 4
        MEAN_ANTI_MISSILE_SPEED: Final[int] = 1000
        VARIANCE_ANTI_MISSILE_SPEED: Final[int] = 3
        COUNT_OF_MISSILES: Final[int] = 50
        NUMBER_OF_ANTI_MISSILES: Final[int] = 6
        DETECTION_DISTANCE: Final[int] = 200
        MEAN_TO_RELOAD: Final[int] = 30
        STANDART_DEVIATION_TO_RELOAD: Final[int] = 2
        MISSILE_SPEED_KM_PER_HOUR: Final[int] = 500
        missile_speed = round(MISSILE_SPEED_KM_PER_HOUR / 60 / 60, 4)
        time_to_hit = round(DETECTION_DISTANCE / missile_speed)
    """

    global COUNT_OF_MISSILES
    global NUMBER_OF_ANTI_MISSILES
    global DETECTION_DISTANCE
    global MEAN_MISSILE_FREQUENCY
    global MEAN_ANTI_MISSILE_SPEED
    global VARIANCE_ANTI_MISSILE_SPEED
    global MEAN_TO_RELOAD
    global STANDART_DEVIATION_TO_RELOAD
    global MISSILE_SPEED_KM_PER_HOUR
    global missile_speed
    global time_to_hit

    print("Введите следующие данные для моделирования...")
    COUNT_OF_MISSILES = int(input("Кол-во вражеских ракет: "))
    NUMBER_OF_ANTI_MISSILES = int(input("Кол-во анти-ракет в каждом ЗРК: "))
    DETECTION_DISTANCE = int(input("Дистанция обнаружения ракет (км): "))
    MEAN_MISSILE_FREQUENCY = int(input("Мат. ожидание для расчёта частоты вылета вражеских ракет (мин): "))
    MEAN_ANTI_MISSILE_SPEED = int(input("Мат. ожидание для расчёта скорости анти-ракет (км/ч): "))
    VARIANCE_ANTI_MISSILE_SPEED = int(input("Дисперсия для расчёта скорости анти-ракет (км/ч): "))
    MEAN_TO_RELOAD = int(input("Мат. ожидание для расчёта времени перезарядки (мин): "))
    STANDART_DEVIATION_TO_RELOAD = int(input("Среднеквадратическое отклонение для расчёта времени перезарядки (мин): "))
    MISSILE_SPEED_KM_PER_HOUR = int(input("Скорость вражеских ракет (км/ч): "))
    missile_speed = round(MISSILE_SPEED_KM_PER_HOUR / 60 / 60, 4)
    time_to_hit = round(DETECTION_DISTANCE / missile_speed)


downed_missiles: list[list[int], list[int]] = [[], []]
count_of_downed_missiles: int = 0
missed_missiles: list[list[int], list[int]] = [[], []]
count_of_missed_missiles: int = 0


def update_count_of_missiles(current_time: int, is_downed: bool):
    global count_of_downed_missiles
    global count_of_missed_missiles
    global downed_missiles
    global missed_missiles

    if is_downed:
        count_of_downed_missiles += 1
    else:
        count_of_missed_missiles += 1
    downed_missiles[0].append(current_time)
    missed_missiles[0].append(current_time)
    downed_missiles[1].append(count_of_downed_missiles)
    missed_missiles[1].append(count_of_missed_missiles)


def show_percentage_of_missiles(downed: int, missed: int):
    print(f"{round(downed / COUNT_OF_MISSILES * 100, 3)}% ракет сбиты")
    print(f"{round(missed / COUNT_OF_MISSILES * 100, 3)}% попали в нашу базу")


def get_time_of_launch(current_time: int) -> int:
    return round(current_time + np.random.exponential(MEAN_MISSILE_FREQUENCY * 60))


def is_aams_ready(aams: dict[str, int]) -> bool:
    return any([aams[key] > 0 for key in list(aams.keys())])


def launch_anti_missile(aams: dict[str, int]) -> str:
    for serial_number in aams.keys():
        if aams[serial_number] > 0:
            aams[serial_number] -= 1
            return serial_number


def get_collision_time(detection_distance: int, missile_speed: float, anti_missile_speed: float) -> int:
    return round(detection_distance / (missile_speed + anti_missile_speed))


def get_anti_missile_speed() -> float:
    return round(np.random.normal(MEAN_ANTI_MISSILE_SPEED / 60 / 60, np.sqrt(VARIANCE_ANTI_MISSILE_SPEED / 60 / 60)), 4)


def get_time_to_reload() -> int:
    return round(np.random.normal(MEAN_TO_RELOAD * 60, STANDART_DEVIATION_TO_RELOAD * 60))


def get_covered_distance(current_time: int, time_until_reload: int) -> int:
    return round(DETECTION_DISTANCE - missile_speed * (time_until_reload - current_time))


def get_nearest_end_of_reload(recharging_aams: dict[int, str], aams: dict[str, int]) -> int:
    reload_time_sorted: list[int] = sorted(list(recharging_aams.keys()))
    for reload_time in reload_time_sorted:
        if aams[recharging_aams[reload_time]] > -NUMBER_OF_ANTI_MISSILES:
            return reload_time
    return np.inf


def write_logs(logs: list[str]) -> None:
    with open("logs.txt", "w") as file:
        file.writelines("%s\n" % log for log in logs)


def build_plot():
    global downed_missiles
    global count_of_downed_missiles
    global missed_missiles
    global count_of_missed_missiles

    downed_missiles[0] = sorted(downed_missiles[0])
    downed_missiles[1] = sorted(downed_missiles[1])
    missed_missiles[0] = sorted(missed_missiles[0])
    missed_missiles[1] = sorted(missed_missiles[1])

    show_percentage_of_missiles(count_of_downed_missiles, count_of_missed_missiles)

    plt.plot(downed_missiles[0], downed_missiles[1])
    plt.plot(missed_missiles[0], missed_missiles[1])
    plt.xlabel("Время (сек)")
    plt.ylabel("Кол-во ракет")
    plt.show()


def start_modeling() -> dict[int, str]:
    missile_launch_times: list[int] = [0]
    [missile_launch_times.append(get_time_of_launch(missile_launch_times[-1])) for _ in range(COUNT_OF_MISSILES - 1)]
    events: dict[int, str] = {}
    [events.update({time_of_launch: Events.LAUNCH_OF_MISSILE.value}) for time_of_launch in missile_launch_times]

    anti_aircraft_missile_systems: dict[str, int] = {
        "aams_1": NUMBER_OF_ANTI_MISSILES,
        "aams_2": NUMBER_OF_ANTI_MISSILES,
        "aams_3": NUMBER_OF_ANTI_MISSILES,
        "aams_4": NUMBER_OF_ANTI_MISSILES
    }
    reloading_aams: dict[int, str] = {}

    for launch_time in missile_launch_times:
        to_del: list[int] = []
        for aams in reloading_aams.items():
            if aams[0] <= launch_time:
                anti_aircraft_missile_systems[aams[1]] += NUMBER_OF_ANTI_MISSILES
                to_del.append(aams[0])
        [reloading_aams.pop(key) for key in to_del]

        if is_aams_ready(anti_aircraft_missile_systems):
            anti_missile_system: str = launch_anti_missile(anti_aircraft_missile_systems)
            if anti_aircraft_missile_systems[anti_missile_system] == 0:
                events[launch_time + get_time_to_reload()] = Events.END_OF_RELOADING.value.format(anti_missile_system)
                reloading_aams[launch_time + get_time_to_reload()] = anti_missile_system
            collision_time: int = get_collision_time(DETECTION_DISTANCE, missile_speed, get_anti_missile_speed())
            events[launch_time + collision_time] = Events.SHOOTING_DOWN.value.format(anti_missile_system)
            update_count_of_missiles(launch_time + collision_time, True)
        else:
            nearest_reload: int = get_nearest_end_of_reload(reloading_aams, anti_aircraft_missile_systems)
            time_until_reload: int = nearest_reload - launch_time
            if time_until_reload < time_to_hit:
                anti_aircraft_missile_systems[reloading_aams[nearest_reload]] -= 1
                if anti_aircraft_missile_systems[reloading_aams[nearest_reload]] == -NUMBER_OF_ANTI_MISSILES:
                    events[nearest_reload + get_time_to_reload()] = Events.END_OF_RELOADING.value.format(reloading_aams[nearest_reload])
                    reloading_aams[nearest_reload + get_time_to_reload()] = reloading_aams[nearest_reload]
                collision_time: int = get_collision_time(get_covered_distance(launch_time, time_until_reload),
                                                         missile_speed,
                                                         get_anti_missile_speed())
                events[nearest_reload + collision_time] = Events.SHOOTING_DOWN.value.format(reloading_aams[nearest_reload])
                update_count_of_missiles(nearest_reload + collision_time, True)
            else:
                events[launch_time + time_to_hit] = Events.HIT.value
                update_count_of_missiles(launch_time + time_to_hit, False)
    build_plot()
    return events
