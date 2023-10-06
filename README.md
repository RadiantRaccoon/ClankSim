# ClankSimulator
A python program simulating the time until max clank for a given deck for TangoTek's Decked Out 2

## Important parameters:
```
DECK = {'sneak': 5, 'evasion': 2, 'loot and scoot': 3, 'clankless': 17} # the deck (does not check for deck validity)
MAX_CLANK = 12 # counted 13 clank before heartbeat started skipping on one of hypno's runs
QUICKDRAW_TIME = 5            # how long it takes to process a card via quickdraw (mostly irrelevant)
PICKUP_TIME = 0 # how many seconds until artifact is picked up (expected)
SHRIEKER_AVERAGE = 0.25 # expected number of shriekers hit every 30 seconds
DISABLE_SHRIEKERS = False # disable clank from shriekers

# program parameters
RUN_COUNT = 1000000

# more program parameters
PRINT_INFO = False      # print additional info about individual runs
DEBUG = 0              # level of debug information
PROFILER = False        # enable profiler
```
Parameters can be edited near the top of the code

Currently available cards: 'sneak', 'clarity', 'evasion', 'loot and scoot', 'second wind', 'beast sense', 'sprint', 'nimble looting', 'smash and grab', 'quickstep', 'eerie silence', 'dungeon repairs', 'swagger', 'eyes on the prize', 'haste', 'silent runner', 'brilliance', 'stumble'
