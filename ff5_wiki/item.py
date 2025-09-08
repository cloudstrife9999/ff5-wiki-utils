from typing import Any
from json import dumps

from ff5_wiki.bestiary import FF5Bestiary
from ff5_wiki.enemy import FF5Enemy
from ff5_wiki.enemy_drop_nature import EnemyDropNature
from ff5_wiki.enemy_steal_nature import EnemyStealNature


class FF5Item():
    __READY_ONLY_ERROR_MSG: str = "This attribute cannot be changed after initialisation."

    def __init__(self, name: str, bestiary: FF5Bestiary) -> None:
        self.__name: str = name
        self.__bestiary: FF5Bestiary = bestiary
        self.__always_dropped_by_prefix: str = "'''Guaranteed drop:''' "
        self.__always_dropped_by: list[FF5Enemy] = []
        self.__commonly_dropped_by_prefix: str = "'''Common drop:''' "
        self.__commonly_dropped_by: list[FF5Enemy] = []
        self.__rarely_dropped_by_prefix: str = "'''Rare drop:''' "
        self.__rarely_dropped_by: list[FF5Enemy] = []
        self.__always_stolen_from_prefix: str = "'''Guaranteed common steal:''' "
        self.__always_stolen_from: list[FF5Enemy] = []
        self.__commonly_stolen_from_prefix: str = "'''Common steal:''' "
        self.__commonly_stolen_from: list[FF5Enemy] = []
        self.__rarely_stolen_from_prefix: str = "'''Rare steal:''' "
        self.__rarely_stolen_from: list[FF5Enemy] = []
        self.__unique_rarely_stolen_from_prefix: str = "'''Unique rare steal:''' "
        self.__unique_rarely_stolen_from: list[FF5Enemy] = []
        self.__newline: str = "<br/>\n"

        self.__populate_enemy_lists()

    @property
    def name(self) -> str:
        '''
        The name of the item.
        '''
        return self.__name

    @name.setter
    def name(self, _: Any) -> None:
        raise AttributeError(FF5Item.__READY_ONLY_ERROR_MSG)

    @property
    def always_dropped_by(self) -> list[FF5Enemy]:
        '''
        List of enemies that drop this item 100% of the time.
        '''
        return self.__always_dropped_by

    @always_dropped_by.setter
    def always_dropped_by(self, _: Any) -> None:
        raise AttributeError(FF5Item.__READY_ONLY_ERROR_MSG)

    @property
    def commonly_dropped_by(self) -> list[FF5Enemy]:
        '''
        List of enemies that commonly drop this item.
        '''
        return self.__commonly_dropped_by

    @commonly_dropped_by.setter
    def commonly_dropped_by(self, _: Any) -> None:
        raise AttributeError(FF5Item.__READY_ONLY_ERROR_MSG)

    @property
    def rarely_dropped_by(self) -> list[FF5Enemy]:
        '''
        List of enemies that rarely drop this item.
        '''
        return self.__rarely_dropped_by

    @rarely_dropped_by.setter
    def rarely_dropped_by(self, _: Any) -> None:
        raise AttributeError(FF5Item.__READY_ONLY_ERROR_MSG)

    @property
    def always_stolen_from(self) -> list[FF5Enemy]:
        '''
        List of enemies that always have this item available as both the common and rare steal.
        '''
        return self.__always_stolen_from

    @always_stolen_from.setter
    def always_stolen_from(self, _: Any) -> None:
        raise AttributeError(FF5Item.__READY_ONLY_ERROR_MSG)

    @property
    def commonly_stolen_from(self) -> list[FF5Enemy]:
        '''
        List of enemies that commonly have this item available as the common steal, and a different item available as the rare steal.
        '''
        return self.__commonly_stolen_from

    @commonly_stolen_from.setter
    def commonly_stolen_from(self, _: Any) -> None:
        raise AttributeError(FF5Item.__READY_ONLY_ERROR_MSG)

    @property
    def rarely_stolen_from(self) -> list[FF5Enemy]:
        '''
        List of enemies that rarely have this item available as the rare steal, and a different item available as the common steal.
        '''
        return self.__rarely_stolen_from

    @rarely_stolen_from.setter
    def rarely_stolen_from(self, _: Any) -> None:
        raise AttributeError(FF5Item.__READY_ONLY_ERROR_MSG)

    @property
    def unique_rarely_stolen_from(self) -> list[FF5Enemy]:
        '''
        List of enemies that have this item available as the rare steal, and no common steal.
        '''
        return self.__unique_rarely_stolen_from

    @unique_rarely_stolen_from.setter
    def unique_rarely_stolen_from(self, _: Any) -> None:
        raise AttributeError(FF5Item.__READY_ONLY_ERROR_MSG)

    def get_wiki_ready_references(self) -> str:
        '''
        Prints the wiki-ready references of all enemies w.r.t. drops and steals for this item.
        '''
        sections: dict[str, list[FF5Enemy]] = {
            self.__always_dropped_by_prefix: self.__always_dropped_by,
            self.__commonly_dropped_by_prefix: self.__commonly_dropped_by,
            self.__rarely_dropped_by_prefix: self.__rarely_dropped_by,
            self.__always_stolen_from_prefix: self.__always_stolen_from,
            self.__commonly_stolen_from_prefix: self.__commonly_stolen_from,
            self.__rarely_stolen_from_prefix: self.__rarely_stolen_from,
            self.__unique_rarely_stolen_from_prefix: self.__unique_rarely_stolen_from
        }

        return self.__newline.join(prefix + ", ".join(enemy.wiki_link_with_custom_text for enemy in enemies) for prefix, enemies in sections.items() if enemies)

    def __populate_enemy_lists(self) -> None:
        for enemy in self.__bestiary.enemies + self.__bestiary.bosses:
            self.__check_stealable_items(enemy=enemy)
            self.__check_droppable_items(enemy=enemy)

    def __check_stealable_items(self, enemy: FF5Enemy) -> None:
        match enemy.steal_nature:
            case EnemyStealNature.COMMON_AND_RARE:
                if enemy.common_steal == self.__name:
                    self.__commonly_stolen_from.append(enemy)
                if enemy.rare_steal == self.__name:
                    self.__rarely_stolen_from.append(enemy)
            case EnemyStealNature.UNIQUE_GUARANTEED:
                if enemy.common_steal == self.__name:
                    self.__always_stolen_from.append(enemy)
            case EnemyStealNature.COMMON_ONLY:
                if enemy.common_steal == self.__name:
                    self.__commonly_stolen_from.append(enemy)
            case EnemyStealNature.RARE_ONLY:
                if enemy.rare_steal == self.__name:
                    self.__unique_rarely_stolen_from.append(enemy)
            case EnemyStealNature.NONE:
                return
            case _:
                raise ValueError(f"Unknown steal nature: {enemy.steal_nature}.")

    def __check_droppable_items(self, enemy: FF5Enemy) -> None:
        match enemy.drop_nature:
            case EnemyDropNature.COMMON_AND_RARE:
                if enemy.common_drop == self.__name:
                    self.__commonly_dropped_by.append(enemy)
                if enemy.rare_drop == self.__name:
                    self.__rarely_dropped_by.append(enemy)
            case EnemyDropNature.UNIQUE_GUARANTEED:
                if enemy.common_drop == self.__name:
                    self.__always_dropped_by.append(enemy)
            case EnemyDropNature.COMMON_ONLY:
                if enemy.common_drop == self.__name:
                    self.__commonly_dropped_by.append(enemy)
            case EnemyDropNature.RARE_ONLY:
                if enemy.rare_drop == self.__name:
                    self.__rarely_dropped_by.append(enemy)
            case EnemyDropNature.NONE:
                return
            case _:
                raise ValueError(f"Unknown drop nature: {enemy.drop_nature}.")

    def __repr__(self) -> str:
        return dumps(
            {
                "Name": self.__name,
                "Always dropped by": [enemy.name for enemy in self.__always_dropped_by],
                "Commonly dropped by": [enemy.name for enemy in self.__commonly_dropped_by],
                "Rarely dropped by": [enemy.name for enemy in self.__rarely_dropped_by],
                "Always stolen from": [enemy.name for enemy in self.__always_stolen_from],
                "Commonly stolen from": [enemy.name for enemy in self.__commonly_stolen_from],
                "Rarely stolen from": [enemy.name for enemy in self.__rarely_stolen_from],
                "Uniquely (rarely) stolen from": [enemy.name for enemy in self.__unique_rarely_stolen_from]
            },
            indent=4
        )

    def __str__(self) -> str:
        return repr(self)
