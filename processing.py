from functools import lru_cache
import uuid

# Where the processing of the data takes place
class Combatant:
    def __init__(self, name, mod, roll, id=None, sign=''):
        self.id = str(uuid.uuid4())
        self.name = name
        self.mod = mod
        self.roll = roll

    def to_json(self):
        return {"id": self.id, "name": self.name, "sign": self.sign, "mod": self.mod, "roll": self.roll}

    # Calculates the Sign of the Number based on if it's positive or negative
    @property
    def sign(self):
        return self._sign(self.mod)

    # Cache the value from the computation of the mod, if it changes then it will store the new result in the cache, otherwise it will spit out the original value
    @lru_cache
    def _sign(self, mod):
        if int(self.mod) >= 0:
            return "+"
        else:
            return ""

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