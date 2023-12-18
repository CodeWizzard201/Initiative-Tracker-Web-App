# Where the processing of the data takes place
class Combatant:
    def __init__(self, name, mod, roll):
        self.name = name
        self.mod = mod
        self.roll = roll
    # Calculates the Sign of the Number based on if it's positive or negative
    def get_sign_(self):
        if self.mod > 0:
            return "+"
        elif self.mod < 0:
            return "-"
        else:
            return ""
    # Getters
    def get_name(self):
        return self.name

    def get_mod(self):
        return self.mod

    def get_roll(self):
        return self.roll


    # Setters for editing
    def set_name(self, value):
        self.name = value

    def set_mod(self, value):
        self.mod = value

    def set_roll(self, value):
        self.roll = value

def make_combatant(name, mod, roll):
    return Combatant(name, mod, roll)