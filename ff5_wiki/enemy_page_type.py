from enum import Enum


class FF5EnemyPageType(Enum):
    PAGE_WITH_FF5_ENEMY_MARKER = 0
    PAGE_WITH_FF5_BOSS_MARKER = 1
    PAGE_WITH_FF5_MARKER = 2
    PAGE_WITH_NO_MARKER = 3
    SPECIAL_CASE = 4
