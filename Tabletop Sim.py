import numpy as np
from random import uniform, randint
import random
random.seed()

def main():
	# rolls = np.zeros(100000)
	# for i in range(100000):
	# 	rolls[i] = randint(1, 20)

	rolls = np.random.randint(1, 21, 100000)
	print("Mean Roll:", np.mean(rolls))

	AC = 19 - 5
	print(AC, ",", (rolls >= AC).sum() / 100000)

	num_trials = 10000
	outcomes = np.zeros(num_trials)
	turns = np.zeros(num_trials)

	num_players = 5

	print("=== Helmed Horror ===")
	for i in range(num_trials):
		players = [Player() for i in range(num_players)]
		enemies = [Nightmare() for i in range(2)]
		outcomes[i], turns[i] = combat(players, enemies)


	print("Mean Players Killed:", outcomes.mean())
	print("Mean Turns Taken:", turns.mean())

	print("=== Plague Knight ===")
	for i in range(num_trials):
		players = [Player() for i in range(num_players)]
		enemies = [PlagueKnight() for i in range(1)]
		outcomes[i], turns[i] = combat(players, enemies)

	print("Mean Players Killed:", outcomes.mean())
	print("Mean Turns Taken:", turns.mean())


class Unit:
	def __init__(self, AC=16, HP=22, prof=2, mod=3, speed=5, range=1, position=0):
		self.AC = AC
		self.HP = HP
		self.proficiency = prof  # self.level // 4 + 2
		self.ability_mod = mod

		self.speed = speed
		self.range = range
		self.position = position

	def attack_roll(self, target_AC):
		roll = randint(1, 20)
		attack = roll + self.proficiency + self.ability_mod
		if roll == 20:
			return 8 + self.ability_mod
		if attack >= target_AC:
			return self.damage_roll()
		return 0

	def damage_roll(self):
		return randint(1, 8) + self.ability_mod

	def damage_received(self, dmg):
		self.HP -= dmg
		return self.HP <= 0

	# returns the index of the enemy to target
	def target(self, enemies, round_log, strategy='random'):
		if strategy == 'random':  # target someone randomly
			pass


class Player(Unit):
	def __init__(self, level=3, AC=16, HP=22, mod=3):
		self.level = level
		proficiency = self.level // 4 + 2
		super().__init__(AC=AC, HP=HP, prof=proficiency, mod=mod)


class Skeleton(Unit):
	def __init__(self):
		super().__init__(AC=13, HP=13, prof=2, mod=2)

	def damage_roll(self):
		return randint(1, 6) + self.ability_mod


class Goblin(Unit):
	def __init__(self):
		super().__init__(AC=15, HP=7, prof=2, mod=3)


class HelmedHorror(Unit):
	def __init__(self):
		super().__init__(AC=19, HP=60, mod=4)

	def damage_roll(self):
		return randint(1, 8) + randint(1, 8) + 8

	def damage_received(self, dmg):
		self.HP -= dmg // 2
		return self.HP <= 0


class Nightmare(Unit):
	def __init__(self):
		super().__init__(AC=13, HP=68, mod=4)

	def damage_roll(self):
		physical = randint(1, 8) + randint(1, 8) + 4
		fire = randint(1, 6) + randint(1, 6)
		return physical + fire


class PlagueKnight(Unit):
	def __init__(self):
		super().__init__(AC=19, HP=80, mod=4)

	def damage_roll(self):
		return randint(1, 8) + randint(1, 8) + 8
		# return randint(1, 10) + self.ability_mod

	def damage_received(self, dmg):
		self.HP -= dmg
		if self.HP <= 0:
			if self.undead_fortitude(dmg):
				self.HP = 1
		return self.HP <= 0

	# currently like Zombie's undead fortitude but the Plague Knight gets advantage on Con saves
	def undead_fortitude(self, dmg_taken):
		con_mod = 3
		check = rollAdv() + con_mod
		DC = 5 + dmg_taken
		return check >= DC


class AnimatedArmor(Unit):
	def __init__(self):
		super().__init__(AC=18, HP=33, prof=2, mod=2)

	def damage_roll(self):
		return 10


# given lists of players and enemies, simulate basic combat
def combat(players, enemies):
	turns = 0
	players_killed = 0
	while len(players) > 0 and len(enemies) > 0:
		for player in players:
			dmg = player.attack_roll(enemies[-1].AC)
			if enemies[-1].damage_received(dmg):
				enemies.pop()
				if len(enemies) == 0:
					return players_killed, turns

		turns += 1
		for enemy in enemies:
			dmg = enemy.attack_roll(players[-1].AC)
			if players[-1].damage_received(dmg):
				players.pop()
				players_killed += 1
				if len(players) == 0:
					return players_killed, turns
	return players_killed, turns



def rollAdv():
	return max(randint(1, 20), randint(1, 20))


if __name__ == "__main__":
	main()