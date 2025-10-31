import math
import random


class Monster:
    def __init__(self, x=0, y=0, energy=1):
        self.x = x
        self.y = y
        self.energy = energy
        self.captured = False

    def __str__(self):
        if not self.captured:
            return f"Monster at ({self.x}, {self.y}), energy: {self.energy}"
        else:
            return f"Monster captured"

    def set_capture_on(self):
        self.captured = True

    def distance_to(self, x2, y2):
        final = round(math.sqrt((x2 - self.x) ** 2 + (y2 - self.y) ** 2))
        return final

    def is_captured(self):
        return self.captured


class Catcher:
    def __init__(self, name="Unknown"):
        self.name = name
        self.energy = 0
        self.x = 0
        self.y = 0
        self.caught_monsters = []

    def __str__(self):
        temp = len(self.caught_monsters)
        return f"Catcher {self.name}: energy = {self.energy}, collected {temp} monster(s)"

    def move_to(self, m):
        self.x = m.x
        self.y = m.y

    def catch_monster(self, m):
        if not m.is_captured():
            self.move_to(m)
            m.set_capture_on()
            self.energy += m.energy
            self.caught_monsters.append(m)

    def get_nearest_monster(self, m_list):
        top_value = None
        top = None
        for i in m_list:
            temp = i.distance_to(self.x, self.y)
            if not i.is_captured():
                if top_value:
                    if temp < top_value:
                        top_value = temp
                        top = i
                else:
                    top_value = temp
                    top = i
        return top


class MonsterMap:
    def __init__(self, catcher1, catcher2):
        self.c1 = catcher1
        print(self.c1)
        self.c2 = catcher2
        print(self.c2)
        self.monsters = []

    def add_monster(self, m):
        self.monsters.append(m)
        print(m)

    def has_remaining_monsters(self):
        for i in self.monsters:
            if not i.is_captured():
                return True
        return False

    def play_game(self):
        while self.has_remaining_monsters():
            m = self.c1.get_nearest_monster(self.monsters)
            if m:
                self.c1.catch_monster(m)
                print(f"{self.c1.name} caught a {m.energy}-energy monster")
            m = self.c2.get_nearest_monster(self.monsters)
            if m:
                self.c2.catch_monster(m)
                print(f"{self.c2.name} caught a {m.energy}-energy monster")

    def announce_winner(self):
        print("--- GAME OVER ---")
        if self.c1.energy == self.c2.energy:
            print("It's a tie!")
        else:
            if self.c1.energy > self.c2.energy:
                print(f"Congratulations! The winner is {self.c1.name} with a total energy of {self.c1.energy}.")
            else:
                print(f"Congratulations! The winner is {self.c2.name} with a total energy of {self.c2.energy}.")


def main():
    print("Welcome to the Monster Hunt Game!")
    name1 = input("Enter the name of the first catcher: ")
    name2 = input("Enter the name of the second catcher: ")
    monster_number = None
    while (not monster_number) or (not (10 >= monster_number >= 0)):
        temp = input("Enter the number of monsters (1-10): ")
        if temp.isnumeric():
            monster_number = int(temp)
    c1 = Catcher(name1)
    c2 = Catcher(name2)
    game = MonsterMap(c1, c2)
    rand = random.Random(30)
    for _ in range(monster_number):
        x = rand.randrange(10)
        y = rand.randrange(10)
        e = rand.randrange(10)
        game.add_monster(Monster(x, y, e))
    game.play_game()
    game.announce_winner()