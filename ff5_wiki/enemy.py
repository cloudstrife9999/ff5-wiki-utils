from string import ascii_lowercase, ascii_uppercase, digits
from typing import Any, Optional
from json import dumps

from ff5_wiki.common import FF5Wiki
from ff5_wiki.enemy_steal_nature import EnemyStealNature
from ff5_wiki.enemy_drop_nature import EnemyDropNature
from ff5_wiki.enemy_page_type import FF5EnemyPageType


class FF5Enemy():
    '''
    A class representing an enemy from Final Fantasy V, useful to keep track of the items it may drop and the items that may be stolen from it.
    '''
    __READY_ONLY_ERROR_MSG: str = "This attribute cannot be changed after initialisation."
    __CHECK_PAGE_EXISTENCE: bool = False  # Already verified them all once; no need to do it again.

    def __init__(self, name: str, is_boss: bool, wiki_page_type: str, common_steal: Optional[str], rare_steal: Optional[str], common_drop: Optional[str], rare_drop: Optional[str]) -> None:
        self.__name: str = self.__validate_enemy_name(name)
        self.__is_boss: bool = is_boss
        self.__wiki_page_type: FF5EnemyPageType = FF5EnemyPageType(int(wiki_page_type))
        self.__wiki_page: str = self.__get_wiki_page()
        self.__wiki_link: str = self.__get_wiki_link()
        self.__wiki_link_with_custom_text: str = self.__get_wiki_link_with_custom_text()
        self.__common_steal: Optional[str] = common_steal
        self.__rare_steal: Optional[str] = rare_steal
        self.__common_drop: Optional[str] = common_drop
        self.__rare_drop: Optional[str] = rare_drop
        self.__steal_nature: EnemyStealNature = self.__determine_steal_nature()
        self.__drop_nature: EnemyDropNature = self.__determine_drop_nature()

    @property
    def name(self) -> str:
        '''
        The name of the enemy.
        '''
        return self.__name

    @name.setter
    def name(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    @property
    def is_boss(self) -> bool:
        '''
        Indicates whether the enemy is a boss.
        '''
        return self.__is_boss

    @is_boss.setter
    def is_boss(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)    

    @property
    def wiki_page(self) -> str:
        '''
        The full URL of the enemy's wiki page.
        '''
        return self.__wiki_page

    @wiki_page.setter
    def wiki_page(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    @property
    def wiki_link(self) -> str:
        '''
        The wiki link for referencing the enemy.
        '''
        return self.__wiki_link

    @wiki_link.setter
    def wiki_link(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    @property
    def wiki_link_with_custom_text(self) -> str:
        '''
        The wiki link for referencing the enemy with custom display text (the unqualified enemy's name).
        '''
        return self.__wiki_link_with_custom_text

    @wiki_link_with_custom_text.setter
    def wiki_link_with_custom_text(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    @property
    def common_steal(self) -> Optional[str]:
        '''
        The common item that can be stolen from the enemy, if any.
        '''
        return self.__common_steal

    @common_steal.setter
    def common_steal(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    @property
    def rare_steal(self) -> Optional[str]:
        '''
        The rare item that can be stolen from the enemy, if any.
        '''
        return self.__rare_steal

    @rare_steal.setter
    def rare_steal(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    @property
    def common_drop(self) -> Optional[str]:
        '''
        The common item that can be dropped by the enemy, if any.
        '''
        return self.__common_drop

    @common_drop.setter
    def common_drop(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    @property
    def rare_drop(self) -> Optional[str]:
        '''
        The rare item that can be dropped by the enemy, if any.
        '''
        return self.__rare_drop

    @rare_drop.setter
    def rare_drop(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    @property
    def steal_nature(self) -> EnemyStealNature:
        '''
        The nature of stealable items the enemy has.
        '''
        return self.__steal_nature

    @steal_nature.setter
    def steal_nature(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    @property
    def drop_nature(self) -> EnemyDropNature:
        '''
        The nature of droppable items the enemy has.
        '''
        return self.__drop_nature

    @drop_nature.setter
    def drop_nature(self, _: Any) -> None:
        raise AttributeError(FF5Enemy.__READY_ONLY_ERROR_MSG)

    def __validate_enemy_name(self, name: str) -> str:
        '''
        Validate and return the enemy name to ensure it follows expected conventions.
        Args:
            name (str): The name of the enemy to validate.
        Returns:
            str: The validated enemy name.
        Raises:
            ValueError: If the enemy name is empty.
            ValueError: If the enemy name is invalid.
        '''
        if not name:
            raise ValueError("Enemy name cannot be empty.")
        elif name in FF5Wiki.SPECIAL_ENEMIES:
            return name
        elif name[0] not in ascii_uppercase:
            raise ValueError(f"Invalid enemy name \"{name}\".")
        elif not all(c in ascii_lowercase + ascii_uppercase + digits + " '.()-#" for c in name):
            raise ValueError(f"Invalid enemy name \"{name}\".")
        else:
            return name

    def __get_wiki_page(self) -> str:
        '''
        Determine and return the full URL of the enemy's wiki page.
        Returns:
            str: The full URL of the enemy's wiki page.
        Raises:
            ValueError: If no appropriate wiki page is found for the enemy.
            AssertionError: If a special enemy's wiki page does not exist.
        '''
        if self.__name in FF5Wiki.SPECIAL_ENEMIES:
            return self.__get_special_enemy_wiki_page()

        page_suffix: str = self.__get_appropriate_wiki_page_suffix()
        candidate: str = f"{FF5Wiki.WIKI_MAIN_URL}{self.__name.split(" (")[0].replace(' ', '_')}{page_suffix}"

        if FF5Wiki.full_page_exists(full_url=candidate, skip=not FF5Enemy.__CHECK_PAGE_EXISTENCE):
            return candidate
        else:
            raise ValueError(f"No appropriate wiki page found for the \"{self.__name}\" enemy. Tried: {candidate}.")

    def __get_appropriate_wiki_page_suffix(self) -> str:
        match self.__wiki_page_type:
            case FF5EnemyPageType.PAGE_WITH_FF5_ENEMY_MARKER:
                return "_(Final_Fantasy_V_enemy)"
            case FF5EnemyPageType.PAGE_WITH_FF5_BOSS_MARKER:
                return "_(Final_Fantasy_V_boss)"
            case FF5EnemyPageType.PAGE_WITH_FF5_MARKER:
                return "_(Final_Fantasy_V)"
            case FF5EnemyPageType.PAGE_WITH_NO_MARKER:
                return ""
            case FF5EnemyPageType.SPECIAL_CASE:
                raise ValueError(f"The \"{self.__name}\" enemy name is marked as a special case. It should have already been handled by another method.")
            case _:
                raise ValueError(f"Could not determine the wiki page for the {self.__name} enemy.")

    def __get_special_enemy_wiki_page(self) -> str:
        '''
        Get the full URL of a special enemy's wiki page. Special enemies are those whose names do not follow the usual naming conventions.
        Returns:
            str: The full URL of the special enemy's wiki page.
        Raises:
            AssertionError: If the special enemy's wiki page does not exist.
        '''
        wiki_page_url: str = f"{FF5Wiki.WIKI_MAIN_URL}{FF5Wiki.SPECIAL_ENEMIES[self.__name]['page_name']}"

        assert FF5Wiki.full_page_exists(full_url=wiki_page_url, skip=not FF5Enemy.__CHECK_PAGE_EXISTENCE), f"The \"{self.__name}\" enemy does not seem to possess a valid wiki page."

        return wiki_page_url

    def __get_wiki_link(self) -> str:
        '''
        Determine and return the wiki link for referencing the enemy. Assumes the enemy name is valid and a wiki page exists.
        Returns:
            str: The wiki link for the enemy.
        '''
        if self.__name in FF5Wiki.SPECIAL_ENEMIES:
            return FF5Wiki.SPECIAL_ENEMIES[self.__name]["wiki_link"]
        else:
            return f"[[{self.__wiki_page.split('/')[-1].replace('_', ' ').replace('%3F', '?')}]]"

    def __get_wiki_link_with_custom_text(self) -> str:
        '''
        Determine and return the wiki link for referencing the enemy with custom display text. Assumes the enemy name is valid and a wiki page exists.
        Returns:
            str: The wiki link for the enemy with custom display text.
        '''
        return self.__wiki_link.replace("]]", f"|{self.__name}]]")

    def __determine_steal_nature(self) -> EnemyStealNature:
        '''
        Determine the nature of stealable items the enemy has based on the common and rare stealable items.
        Returns:
            EnemyStealNature: The nature of stealable items.
        '''
        if self.__common_steal and self.__rare_steal:
            return EnemyStealNature.COMMON_AND_RARE if self.__common_steal != self.__rare_steal else EnemyStealNature.UNIQUE_GUARANTEED
        elif self.__common_steal:
            return EnemyStealNature.COMMON_ONLY
        elif self.__rare_steal:
            return EnemyStealNature.RARE_ONLY
        else:
            return EnemyStealNature.NONE

    def __determine_drop_nature(self) -> EnemyDropNature:
        '''
        Determine the nature of droppable items the enemy has based on the common and rare droppable items.
        Returns:
            EnemyDropNature: The nature of droppable items.
        '''
        if self.__common_drop and self.__rare_drop:
            return EnemyDropNature.COMMON_AND_RARE if self.__common_drop != self.__rare_drop else EnemyDropNature.UNIQUE_GUARANTEED
        elif self.__common_drop:
            return EnemyDropNature.COMMON_ONLY
        elif self.__rare_drop:
            return EnemyDropNature.RARE_ONLY
        else:
            return EnemyDropNature.NONE

    def __repr__(self) -> str:
        return dumps({
            "name": self.__name,
            "is_boss": self.__is_boss,
            "wiki_page": self.__wiki_page,
            "wiki_link": self.__wiki_link,
            "wiki_link_with_custom_text": self.__wiki_link_with_custom_text,
            "common_steal": self.__common_steal,
            "rare_steal": self.__rare_steal,
            "common_drop": self.__common_drop,
            "rare_drop": self.__rare_drop,
            "steal_nature": self.__steal_nature.name,
            "drop_nature": self.__drop_nature.name
        }, indent=4)

    def __str__(self) -> str:
        return repr(self)
