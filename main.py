#!/usr/bin/env python3

from ff5_wiki.bestiary import FF5Bestiary
from ff5_wiki.common import FF5Wiki
from ff5_wiki.item import FF5Item


if __name__ == "__main__":
    bestiary = FF5Bestiary(enemy_list_file=FF5Wiki.ENEMY_FILE, boss_list_file=FF5Wiki.BOSS_FILE)
    item_list: list[str] = []

    with open(FF5Wiki.ITEM_FILE, "r") as i_f:
        for elm in i_f.readlines():
            if len(elm) > 1:
                item_list.append(elm.strip())

    for elm in item_list:
        ff5_item: FF5Item = FF5Item(name=elm, bestiary=bestiary)

        print(ff5_item.name)
        print(ff5_item.get_wiki_ready_references())
        print("----------")
