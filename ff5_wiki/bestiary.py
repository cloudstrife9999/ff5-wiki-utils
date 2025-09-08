from typing import Any
from csv import reader

from ff5_wiki.enemy import FF5Enemy


class FF5Bestiary():
    '''
    Represents the bestiary in Final Fantasy V.
    This class is used to manage and retrieve information about enemies in the game.
    '''
    __READY_ONLY_ERROR_MSG: str = "This attribute cannot be changed after initialisation."
    __BESTIARY_LINE_LENGTH: int = 6  # Expected number of columns in the bestiary CSV files.

    def __init__(self, enemy_list_file: str, boss_list_file: str) -> None:
        self.__enemies: list[FF5Enemy] = self.__init_enemies(enemy_list_file=enemy_list_file, boss_flag=False)
        self.__bosses: list[FF5Enemy] = self.__init_enemies(enemy_list_file=boss_list_file, boss_flag=True)

    @property
    def enemies(self) -> list[FF5Enemy]:
        '''
        Returns the list of regular enemies in the bestiary.
        '''
        return self.__enemies

    @enemies.setter
    def enemies(self, _: Any) -> None:
        raise AttributeError(FF5Bestiary.__READY_ONLY_ERROR_MSG)

    @property
    def bosses(self) -> list[FF5Enemy]:
        '''
        Returns the list of bosses in the bestiary.
        '''
        return self.__bosses

    @bosses.setter
    def bosses(self, _: Any) -> None:
        raise AttributeError(FF5Bestiary.__READY_ONLY_ERROR_MSG)

    @property
    def all_enemies(self) -> list[FF5Enemy]:
        '''
        Returns a combined list of all enemies and bosses in the bestiary.
        '''
        return self.__enemies + self.__bosses

    @all_enemies.setter
    def all_enemies(self, _: Any) -> None:
        raise AttributeError(FF5Bestiary.__READY_ONLY_ERROR_MSG)

    def __init_enemies(self, enemy_list_file: str, boss_flag: bool) -> list[FF5Enemy]:
        enemies: list[FF5Enemy] = []

        with open(enemy_list_file, "r") as i_f:
            for line in reader(i_f):
                if not line or len(line) != FF5Bestiary.__BESTIARY_LINE_LENGTH or line[0] == "Name":
                    continue

                name, wiki_page_type, common_steal, rare_steal, common_drop, rare_drop = line

                if name:
                    enemies.append(FF5Enemy(name=name, is_boss=boss_flag, wiki_page_type=wiki_page_type, common_steal=common_steal, rare_steal=rare_steal, common_drop=common_drop, rare_drop=rare_drop))

        return enemies
