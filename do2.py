# Clank simulator for TangoTek's Decked Out 2
# Neglects shriekers, but in general, a shrieker reduces dungeon time by 1 minute

import random
import cProfile
import pstats
from tqdm import tqdm
import numpy as np
# import matplotlib.pyplot as plt

# Decked Out parameters

# Cards should be input in the form {'card name in lowercase': card_count}
# cards that can never affect clank can be put into the clankless category
# but the code should not break if the cards are added anyway
DECK = {'sneak': 5, 'evasion': 2, 'loot and scoot': 3, 'clankless': 17} 
MAX_CLANK = 20 
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

class DeckedOutSimulator:
    def __init__(self, deck):
        self.deck = deck
        self.reset()

        self.card_actions = {
            'sneak': self.process_sneak,
            'clarity': self.process_clarity,
            'evasion': self.process_evasion,
            'loot and scoot': self.process_speed,
            'second wind': self.process_speed,
            'beast sense': self.process_beast,
            'sprint': self.process_sprint,
            'nimble looting': self.process_nimble,
            'smash and grab': self.process_smash,
            'quickstep': self.process_quickstep,
            'eerie silence': self.process_eerie,
            'dungeon repairs': self.process_dungeon_repairs,
            'swagger': self.process_swagger,
            'eyes on the prize': self.process_eyes,
            'haste': self.process_haste,
            'brilliance': self.process_brilliance,
            'stumble': self.process_stumble
        }

    # resets simulator to initial state
    def reset(self):
        self.cards = []
        self.nimble_looting = False
        self.eerie_silence = False
        self.silent_runner = False
        self.clanked_out = False
        self.artifact = False
        self.haste = 0
        self.time = 0
        self.clank = 0
        self.clank_block = 0
        self.last_stumble = -60 # stumbles are added at minute 1,3,5 etc
        self.shrieker_average = SHRIEKER_AVERAGE

        for card in self.deck:
            if card == 'silent runner':
                self.silent_runner = True
            else:
                self.cards.extend([card] * self.deck[card])
        random.shuffle(self.cards)

    # run simulations of runs, returns list of max clank times
    # and whether the artifact was picked up before max clank
    def run_simulation(self, iterations=1):
        times = []
        for _ in tqdm(range(0, iterations), desc='Iterations', ascii=False, ncols=100):
            while not self.clanked_out:
                if self.time > PICKUP_TIME:
                    self.simulate_artifact_pickup()
                self.simulate_step()
            times.append((self.time, self.artifact))
            self.reset()
        return times

    def simulate_artifact_pickup(self):
        if not self.artifact:
            self.process_clank(3)
            self.artifact = True

    def simulate_step(self):
        self.time += int(30 * (1 - 0.1 * self.haste))
        if self.time - self.last_stumble >= 120:
            self.cards.append('stumble')
            random.shuffle(self.cards)
            self.last_stumble += 120

        # simulate shriekers going off
        if not DISABLE_SHRIEKERS:
            shrieks = np.random.poisson(self.shrieker_average, 1)[0]
            self.process_clank(shrieks)

        self.process_card()

    def process_sneak(self):
        self.clank_block += 2
    
    def process_clarity(self):
        self.clank_block += 2

    def process_evasion(self):
        self.clank_block += 4
    
    # length is number of 15 second increments
    def process_speed(self, length = 1):
        if self.silent_runner:
            for _ in range(0, length):
                if random.random() > 0.5:
                    self.clank_block += 1

    def process_beast(self):
        self.process_clank(1)

    def process_sprint(self):
        for _ in range(0, 4):
            self.process_speed()

    def process_nimble(self):
        self.nimble_looting = True
        self.clank_block += 1

    def process_smash(self):
        self.process_clank(2)

    def process_quickstep(self):
        self.clank_block += 2
        self.process_speed()
        self.process_card()
        self.time += QUICKDRAW_TIME

    def process_eerie(self):
        self.eerie_silence = True
        self.clank_block += 8

    def process_dungeon_repairs(self):
        self.process_clank(1)

    def process_swagger(self):
        self.cards.append('stumble')
        self.cards.append('stumble')

    def process_eyes(self):
        self.process_clank(2)

    def process_haste(self):
        self.haste += 1

    def process_brilliance(self):
        self.process_card()
        self.time += QUICKDRAW_TIME
        self.process_card()
        self.time += QUICKDRAW_TIME
    
    def process_stumble(self):
        self.process_clank(2)

    # draw a card and process its effects
    def process_card(self):
        # if no cards are present during a draw, nothing happens
        if len(self.cards) == 0:
            return
        
        card = self.cards.pop()

        # check for eerie silence
        if self.eerie_silence:
            self.eerie_silence = False
            return
        
        # process card
        action = self.card_actions.get(card)
        if action:
            action()
        else:
            if card != 'clankless':
                print(f'Unrecognized card {card}')
        

    # simulate adding count clank to current clank and clank block
    def process_clank(self, count):
        for _ in range(0, count):
            if self.clank_block > 0:
                if self.nimble_looting:
                    pass
                self.clank_block -= 1
            else:
                self.nimble_looting = False
                self.clank += 1

        if self.clank >= MAX_CLANK:
            self.clanked_out = True
            if PRINT_INFO > 0:
                print(f'Max clank reached at {self.time // 60} minutes, {self.time % 60} seconds')
                print(f'{len(self.cards)} cards remain')
                if len(self.cards) > 0:
                    print(f'Remaining cards are: {self.cards}')

def main():
    profiler = cProfile.Profile()
    if PROFILER:
        profiler.enable()

    print(f'Simulating {RUN_COUNT} decked out runs...')
    sim = DeckedOutSimulator(DECK)
    runs = {}
    results = sim.run_simulation(RUN_COUNT)
    raw_results = [x[0] for x in results]
    for x in raw_results:
        if x in runs.keys():
            runs[x] += 1
        else:
            runs[x] = 1

    sorted_runs = dict(sorted(runs.items()))
    for key, val in sorted_runs.items():
        print(f'{time_as_string(key)}: {val}')

    # plt.boxplot(raw_results, vert=False, autorange=True, meanline=True)
    # plt.xlabel('Time to max clank (seconds)')
    # # plt.ylabel('Runs')
    # plt.show()

    if PROFILER:
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative').print_stats(10)

def time_as_string(i):
    return f'{i // 3600} hours, {(i % 3600) // 60} minutes, {i % 60} seconds'

if __name__ == '__main__':
    main()