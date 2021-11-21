from enum import Enum


class Events(Enum):
    LAUNCH_OF_MISSILE: str = "Вражеская ракета обнаружена"
    SHOOTING_DOWN: str = "Вражеская ракета сбита из ЗРК {}"
    HIT: str = "Вражеская ракета попала в нашу базу"
    END_OF_RELOADING: str = "ЗРК {} перезаряжен"
