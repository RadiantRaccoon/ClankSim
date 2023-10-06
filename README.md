# ClankSimulator
A python program simulating the time until max clank for a given deck for TangoTek's Decked Out 2

## Important parameters:
```
SHRIEKER_CHANCE = 0.25 # expected number of shriekers hit every 2 minutes
MAX_CLANK = 12 # counted 13 clank before heartbeat started skipping on one of hypno's runs, but not sure
QUICKDRAW_TIME = 5            # how long it takes to process a card via quickdraw (unknown)
PICKUP_TIME = 0 # how many seconds until artifact is picked up (expected)
RUN_COUNT = 10000 # number of runs to simulate
```
Parameters can be edited near the top of the code

Currently available cards: 'sneak', 'clarity', 'evasion', 'loot and scoot', 'second wind', 'beast sense', 'sprint', 'nimble looting', 'smash and grab', 'quickstep', 'eerie silence', 'dungeon repairs', 'swagger', 'eyes on the prize', 'haste', 'silent runner', 'brilliance', 'stumble'
