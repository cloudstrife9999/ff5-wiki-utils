from enum import Enum


class EnemyStealNature(Enum):
    '''
    Enumeration representing the different types of stealable items an enemy can have.
    - COMMON_AND_RARE: Both common and rare stealable items are present and different.
    - UNIQUE_GUARANTEED: The common and rare stealable items are the same (guaranteed steal).
    - COMMON_ONLY: Only the common stealable item is present, and the rare stealable item is None.
    - RARE_ONLY: The common stealable item is None and the rare stealable item is not None.
    - NONE: No stealable items are present.
    '''
    COMMON_AND_RARE = 0
    UNIQUE_GUARANTEED = 1
    COMMON_ONLY = 2
    RARE_ONLY = 3
    NONE = 4
