class Hero:
    def __init__(self, name, hp=100, damage=15):
        self.name = name
        self.hp = hp
        self.damage = damage
    def attack(self, target):
        self.target = target
        self.target.hp -= self.damage
        print(f"{self.name} ударил {self.target.name} на {self.damage} урона!, hp {self.target.name} = {self.target.hp}")
        if self.target.hp <= 0:
            print(f"{self.target.name} пал в бою")
    def is_alive(self):
        if self.hp > 0:
            return True
        else:
            return False
    def __str__(self):
        return f"{self.name} | HP: {self.hp}"

class Arena:
    def __init__(self, heroes=[]):
        self.heroes = heroes
    def add_hero(self, hero):
        self.heroes.append(hero)
    def start_fight(self, hero1_name, hero2_name):
        hero1 = None
        hero2 = None
        for hero in self.heroes:
            if hero.name == hero1_name:
                hero1 = hero
            if hero.name == hero2_name:
                hero2 = hero
            if hero1 and hero2:
                while hero1.is_alive() and hero2.is_alive():
                    hero1.attack(hero2)
                    if not hero2.is_alive():
                        break
                    hero2.attack(hero1)
                    if not hero1.is_alive():
                        break

    def show_heroes(self):
        for i, target in enumerate(self.heroes, start=1):
            print(f"{i}: {target.name}")
        #print(f"{i}: {name.name} "for i, name in self.heroes)

arena = Arena()
arena.add_hero(Hero("Рыцарь", damage=20))
arena.add_hero(Hero("Орк", damage=10))

arena.show_heroes()
arena.start_fight("Рыцарь", "Орк")



