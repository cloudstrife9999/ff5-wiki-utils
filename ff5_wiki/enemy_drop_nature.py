from enum import Enum


class EnemyDropNature(Enum):
    '''
    Enumeration representing the different types of droppable items an enemy can have.
    - COMMON_AND_RARE: Both common and rare droppable items are present and different.
    - UNIQUE_GUARANTEED: The common and rare droppable items are the same (guaranteed drop).
    - COMMON_ONLY: Only the common droppable item is present, and the rare droppable item is None.
    - RARE_ONLY: The common droppable item is None and the rare droppable item is not None.
    - NONE: No droppable items are present.
    '''
    COMMON_AND_RARE = 0
    UNIQUE_GUARANTEED = 1
    COMMON_ONLY = 2
    RARE_ONLY = 3
    NONE = 4
