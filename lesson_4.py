from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.health} damage: {self.damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes: list):
        hero: Hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes: list):
        for hero in heroes:
            if hero.name == "gerald":  # Пропускаем атакующего Ведьмака
                if hero.health > 0:  # Но Ведьмак все равно получает урон
                    hero.health -= self.damage
                continue  # Пропускаем Ведьмака, чтобы он не наносил урон
            if hero.health > 0:
                if type(hero) == Berserk and self.defence != hero.ability:
                    hero.blocked_damage = choice([5, 10])
                    hero.health -= (self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss: Boss):
        boss.health -= self.damage

    def apply_super_power(self, boss: Boss, heroes: list):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss: Boss, heroes: list):
        crit = randint(2, 5) * self.damage
        boss.health -= crit
        print(f'Warrior {self.name} hit critically {crit}')

class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')

    def apply_super_power(self, boss: Boss, heroes: list):
        # TODO Here will be implementation of Boosting
        pass


class Healer(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss: Boss, heroes: list):
        for hero in heroes:
            if hero.health > 0 and hero != self:
                hero.health += self.__heal_points


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss: Boss, heroes: list):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted {self.blocked_damage} damage to boss.')

class Wither(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'REVIVE')
        self.__used = False

    def apply_super_power(self, boss: Boss, heroes: list):
        if not self.__used:
            for hero in heroes:
                if hero.health == 0:
                    hero.health = hero.health + self.health
                    self.health = 0
                    self.__used = True
                    print(f'Wither {self.name} отдал свою жизнь за {hero.name}')
                    break
class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')
        self.rounds_left = 4

    def apply_super_power(self, boss: Boss, heroes: list):
        if self.rounds_left > 0:
            for hero in heroes:
                if hero.health > 0:
                    hero.damage += 20
            self.rounds_left -= 1
            print(f'Magic {self.name} увеличил урон всех героев на 20! Осталось {self.rounds_left} раундов.')
class Hacker(Hero):
    def __init__(self, name, health, damage, steal_amount):
        super().__init__(name, health, damage, 'STEAL_HEALTH')
        self.__steal_amount = steal_amount

    @property
    def steal_amount(self):
        return self.__steal_amount

    def apply_super_power(self, boss: Boss, heroes: list):
        if boss.health > 0:
            stolen_health = min(self.steal_amount, boss.health)
            boss.health -= stolen_health
            print(f'Hacker {self.name} забрал {stolen_health} здоровья у босса.')
            alive_heroes = [hero for hero in heroes if hero.health > 0]
            if alive_heroes:
                hero = choice(alive_heroes)
                hero.health += stolen_health
                print(f'Hacker {self.name} передал {stolen_health} здоровья {hero.name}.')

round_number = 0


def play_round(boss: Boss, heroes: list):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def is_game_over(boss: Boss, heroes: list):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def start_game():
    boss = Boss('Fuse', 1000, 50)

    warrior_1 = Warrior('Anton', 280, 10)
    warrior_2 = Warrior('Akakii', 270, 15)
    magic = Magic('Itachi', 290, 10)
    doc = Healer('Aibolit', 250, 5, 15)
    assistant = Healer('Dulittle', 300, 5, 5)
    berserk = Berserk('Guts', 260, 10)
    witcher = Wither("gerald",400,0)
    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant,witcher]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


def show_statistics(boss: Boss, heroes: list):
    print(f'ROUND {round_number} -----------------')
    print(boss)
    for hero in heroes:
        print(hero)


start_game()
