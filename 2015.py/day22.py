from itertools import product


class Spell:
    def __init__(self, name, cost, dmg=0, heal=0, armor=0, mana=0, duration=0):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.heal = heal
        self.armor = armor
        self.mana = mana
        self.duration = duration

    def __repr__(self):
        return f"{self.name} with {self.duration} rounds left"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class MagicMissile(Spell):
    def __init__(self):
        super().__init__("Magic Missle", cost=53, dmg=4)


class Drain(Spell):
    def __init__(self):
        super().__init__("Drain", cost=73, dmg=2, heal=2)


class Shield(Spell):
    def __init__(self):
        super().__init__("Shield", cost=113, armor=7, duration=6)


class Poison(Spell):
    def __init__(self):
        super().__init__("Poison", cost=173, dmg=3, duration=6)


class Recharge(Spell):
    def __init__(self):
        super().__init__("Recharge", cost=229, mana=101, duration=5)


SPELLS = [MagicMissile, Drain, Shield, Poison, Recharge]


class Boss:
    def __init__(self, hp, dmg):
        self.hp = hp
        self.dmg = dmg

    def __repr__(self):
        return f"Boss remaining hp: {self.hp}"


class Player:
    def __init__(self, hp, mana):
        self.hp = hp
        self.mana = mana
        self.spent = 0
        self.dmg = 0
        self.armor = 0
        self.spells = set()

    def __repr__(self):
        return (
            f"Player remaining hp: {self.hp}\n"
            f"Player remaining mana: {self.mana}\n"
            "Active Spells:\n" + "\n".join([str(spell) for spell in self.spells])
        )

    def cast_spell(self, spell, boss):
        self.mana -= spell.cost
        self.spent += spell.cost

        if spell.duration > 0:
            self.spells.add(spell)
        else:
            boss.hp -= spell.dmg
            self.hp += spell.heal

    def remove_inactive_spell(self):
        self.spells = set(filter(lambda x: x.duration > 0, self.spells))

    def player_turn(self, boss):
        self.remove_inactive_spell()

        self.hp += sum(spell.heal for spell in self.spells)
        self.mana += sum(spell.mana for spell in self.spells)
        dmg = self.dmg + sum(spell.dmg for spell in self.spells)

        boss.hp -= dmg

        for spell in self.spells:
            spell.duration -= 1

    def boss_turn(self, boss):
        self.remove_inactive_spell()

        self.player_turn(boss)
        armor = self.armor + sum(spell.armor for spell in self.spells)
        self.hp -= max(1, boss.dmg - armor)


def spell_factory(spells):
    str_to_spell = {"M": MagicMissile, "D": Drain, "S": Shield, "P": Poison, "R": Recharge}
    return [str_to_spell[i]() for i in spells]


MIN_SPENT = 10000


def simulate(spells):
    global MIN_SPENT
    player = Player(50, 500)
    boss = Boss(55, 8)

    for spell in spells:
        # part 2
        if player.hp <= 1:
            return
        player.hp -= 1

        player.player_turn(boss)
        player.remove_inactive_spell()

        if boss.hp <= 0:
            MIN_SPENT = min(MIN_SPENT, player.spent)
            return

        if (
            spell.cost > player.mana
            or spell in player.spells
            or player.spent + spell.cost > MIN_SPENT
        ):
            return
        player.cast_spell(spell, boss)

        if boss.hp <= 0:
            MIN_SPENT = min(MIN_SPENT, player.spent)
            return

        player.boss_turn(boss)

        if boss.hp <= 0:
            MIN_SPENT = min(MIN_SPENT, player.spent)
            return
        if player.hp <= 0:
            return


for spells in product("MDSPR", repeat=9):
    simulate(spell_factory(spells))

print(MIN_SPENT)
