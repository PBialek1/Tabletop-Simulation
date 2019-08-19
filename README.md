# Tabletop-Simulation
When main() is run, the program will run trials of combat simulations. At the beginning of each trial, a party of players will go up against a party of monsters. The two parties will take turns making basic attacks against the first creature in the opposed party. The attacker will make a 1d20 roll vs the target's AC adding their proficency bonus and ability modifier. If they hit, they will then roll damage, which is then subtracted from the target's HP. If a creature's HP is reduced to zero or less, they are removed from the combat. This process repeats until one party has no creatures left.  
Currently, the two metrics I am tracking for the purposes of balancing monsters are Mean Turns Taken and Mean Players Killed. I have not found any metrics that correlate closely to Challenge Rating.
