import threading
from functools import lru_cache
from datetime import datetime

id_lock = threading.Lock()
# Where the processing of the data takes place
class Combatant:
    def __init__(self, name, mod, roll, id=None, sign=''):
        with id_lock:
            self.id = generate_id() if id is None else id
        self.name = name
        self.mod = int(mod)
        self.roll = int(roll)

    def to_json(self):
        return {"id": self.id, "name": self.name, "sign": self.sign, "mod": self.mod, "roll": self.roll}

    # Calculates the Sign of the Number based on if it's positive or negative
    @property
    def sign(self):
        return self._sign(self.mod)

    # Cache the value from the computation of the mod, if it changes then it will store the new result in the cache, otherwise it will spit out the original value
    @lru_cache
    def _sign(self, mod):
        if self.mod >= 0:
            return "+"
        else: # Only negative numbers are here
            return " "

def generate_id():
    current_time = datetime.now().timestamp() * 1000
    timestamp = str(int(current_time))
    return f"combatant_{timestamp}"

#Sorts depending on which two settings are selected on the page
def sort_combatants(array, descending, tiebreaker):
    if descending and tiebreaker:
        #Do descending sorting with tiebreaker
        array.sort(key=lambda x:(x.roll, x.mod), reverse=True)
    elif descending:
        #Do descending sorting with no tiebreaker
        array.sort(key=lambda x:x.roll, reverse=True)
    elif tiebreaker:
        #Do ascending sorting with tiebreaker
        array.sort(key=lambda x:(x.roll, x.mod))
    else:
        #Do ascending sorting with no tiebreaker
        array.sort(key=lambda x:x.roll)

def make_combatant(name, mod, roll):
    return Combatant(name, mod, roll)