from requests import head


class FF5Wiki():
    ENEMY_FILE: str = "ff5_wiki/enemies.csv"
    BOSS_FILE: str = "ff5_wiki/bosses.csv"
    ITEM_FILE: str = "ff5_wiki/items.txt"

    WIKI_MAIN_URL: str = "https://finalfantasy.fandom.com/wiki/"

    # The order of these suffixes matters.
    # This is because less specific suffixes might refer to pages non-specific to Final Fantasy V enemies.
    # Bosses suffixes are checked after enemy suffixes to avoid unnecessary checks).
    # The empty suffix is checked last as a fallback for FFV-unique enemy names.
    # If a new suffix is added, please ensure it is in the correct place.
    WIKI_ENEMY_SUFFIXES: dict[str, str] = {
        "_(Final_Fantasy_V_enemy)": " (Final Fantasy V enemy)",
        "_(Final_Fantasy_V_boss)": " (Final Fantasy V boss)",
        "_(Final_Fantasy_V)": " (Final Fantasy V)",
        "": ""
    }

    # Special cases where the enemy name does not follow the usual naming conventions.
    # The key is the enemy name, and the value is a dictionary containing "page_name" and "wiki_link".
    SPECIAL_ENEMIES: dict[str, dict[str, str]] = {
        "???": {
            "page_name": r"%3F%3F%3F_(Final_Fantasy_V)",
            "wiki_link": "[[??? (Final Fantasy V)|???]]"
        },
        "Hole (boss)": {
            "page_name": "Hole_(Sandworm_battle)",
            "wiki_link": "[[Hole (Sandworm battle)|Hole]]"
        },
        "Launcher (boss #260)": {
            "page_name": "Launcher_(Soul_Cannon)",
            "wiki_link": "[[Launcher (Soul Cannon)|Launcher (boss #260)]]"
        },
        "Launcher (boss #261)": {
            "page_name": "Launcher_(Soul_Cannon)",
            "wiki_link": "[[Launcher (Soul Cannon)|Launcher (boss #261)]]"
        },
        "Exdeath (Great Forest of Moore - boss)": {
            "page_name": "Exdeath_(boss)",
            "wiki_link": "[[Exdeath (boss)|Exdeath (Great Forest of Moore - boss)]]"
        },
        "Exdeath (boss #285)": {
            "page_name": "Exdeath_(boss)",
            "wiki_link": "[[Exdeath (boss)|Exdeath (boss #285)]]"
        },
        "Exdeath (boss #313)": {
            "page_name": "Exdeath_(tree form)",
            "wiki_link": "[[Exdeath (tree form)|Exdeath (boss #313)]]"
        },
        "Launcher (boss #318)": {
            "page_name": "Launcher_(Guardian)",
            "wiki_link": "[[Launcher (Guardian)|Launcher (boss #318)]]"
        },
        "Launcher (boss #319)": {
            "page_name": "Launcher_(Guardian)",
            "wiki_link": "[[Launcher (Guardian)|Launcher (boss #319)]]"
        }
    }

    @staticmethod
    def page_exists(title: str, skip: bool=False) -> bool:
        '''
        May check if a wiki page exists from its title. A HEAD request is used to avoid downloading the entire page content.
        Args:
            title (str): The title of the wiki page to check.
            skip (bool): If True, the function will always return True without checking. Defaults to False.
        Returns:
            bool: True if the page exists, False otherwise.
        '''
        if skip:
            return True
        else:
            return head(f"{FF5Wiki.WIKI_MAIN_URL}{title}").status_code == 200

    @staticmethod
    def full_page_exists(full_url: str, skip: bool=False) -> bool:
        '''
        May check if a wiki page exists given its full URL. A HEAD request is used to avoid downloading the entire page content.
        Args:
            full_url (str): The full URL of the wiki page to check.
            skip (bool): If True, the function will always return True without checking. Defaults to False.
        Returns:
            bool: True if the page exists, False otherwise.
        '''
        if skip:
            return True
        else:
            return head(full_url).status_code == 200
