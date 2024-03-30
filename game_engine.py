import random
from collections import defaultdict

class Player:
    def __init__(self, strategy, name):
        self.strategy = strategy
        self.name = name
        self.points = 0
        self.reset_for_new_game()
        # Initialize for strategies requiring predefined orders or indices
        self.position_order = [4, 2, 6, 1, 3, 5]  # Logical numbering
        self.color_order = [4, 2, 6, 1, 3, 5]  # Logical numbering
        # Track the last guess to determine the next step
        self.last_position_index = -1  # Tracks the last position guessed
        self.last_color_index = -1  # Tracks the last color guessed
    
    def add_point(self):
        self.points += 1

    def guess(self, remaining_colors, remaining_positions):
        if self.strategy == "random":
            return random.choice(remaining_colors), random.choice(remaining_positions)
        
        elif self.strategy == "Colton_special":
            if self.color_index >= len(remaining_colors):
                self.color_index = 0
            if self.position_index >= len(remaining_positions):
                self.position_index = 0
            
            guess_color = remaining_colors[self.color_index]
            guess_position = remaining_positions[self.position_index]
            
            self.color_index += 1
            self.position_index += 1
            
            return guess_color, guess_position
        
        elif self.strategy == "smart_random":
            # Generate all possible current guesses
            possible_guesses = [(color, position) for color in remaining_colors for position in remaining_positions]
            # Filter out already guessed combinations
            new_guesses = [guess for guess in possible_guesses if guess not in self.previous_guesses]
            if new_guesses:
                chosen_guess = random.choice(new_guesses)
                self.previous_guesses.add(chosen_guess)
                return chosen_guess
            else:
                # Fallback in case all combinations are exhausted (shouldn't happen in normal gameplay)
                return None, None
            
        elif self.strategy == "position_search" or self.strategy == "color_search":
            guess = self.binary_search_like_guess(remaining_colors, remaining_positions)
            if guess:
                return guess
            # Fallback if no guess is made
            return remaining_colors[0], remaining_positions[0] if remaining_colors and remaining_positions else (None, None)

    def reset_for_new_game(self):
        self.points = 0
        self.color_index = 0
        self.position_index = 0
        self.previous_guesses = set()  # Reset previous guesses for "smart_random"
        # Reset these for a new game
        self.last_position_index = -1
        self.last_color_index = -1

    def binary_search_like_guess(self, remaining_colors, remaining_positions):
        if self.strategy == "position_search":
            # Move to the next position in the order
            self.last_position_index = (self.last_position_index + 1) % len(self.position_order)
            next_position = self.position_order[self.last_position_index]
            if next_position in remaining_positions:
                selected_position = next_position
                selected_color = remaining_colors[0]  # Pick the first available color
                return selected_color, selected_position
        
        elif self.strategy == "color_search":
            # Move to the next color in the order
            self.last_color_index = (self.last_color_index + 1) % len(self.color_order)
            if self.last_color_index < len(remaining_colors):
                selected_color = remaining_colors[self.last_color_index]
                selected_position = remaining_positions[0]  # Pick the first available position
                return selected_color, selected_position

            # Reset if end of list reached or no valid guess could be made
            return None
    
class Game:
    def __init__(self, players):
        self.players = players
        self.colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
        self.positions = list(range(1, 7))  # Positions 1 through 6
        self.correct_assignments = {}
        self.initialize_game()
    
    def initialize_game(self):
        random.shuffle(self.colors)
        for position, color in zip(self.positions, self.colors):
            self.correct_assignments[position] = color
    
    def play_round(self):
        random.shuffle(self.players)  # Shuffle players each round for fairness
        for player in self.players:
            guess_color, guess_position = player.guess(self.colors, self.positions)
            if self.correct_assignments[guess_position] == guess_color:
                player.add_point()
                self.colors.remove(guess_color)
                self.positions.remove(guess_position)
                if len(self.colors) == 0:  # Last drink guessed correctly
                    return True  # Game over
        return False  # Game continues
    
    def play_game(self):
        while not self.play_round():
            pass
        game_results = {player.name: player.points for player in self.players}
        # Reset for next game
        for player in self.players:
            player.reset_for_new_game()  # Corrected to call the right method
        self.colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
        self.positions = list(range(1, 7))
        self.initialize_game()
        return game_results

class Simulation:
    def __init__(self, num_games, player_strategies):
        self.num_games = num_games
        self.players = [Player(strategy, f"Player {i+1}") for i, strategy in enumerate(player_strategies)]
        self.stats = defaultdict(int)
        #self.seed = 42
    
    def run(self):
        # if self.seed is not None:
        #     random.seed(self.seed)  # Set the seed for the random number generator

        game = Game(self.players)
        for _ in range(self.num_games):
            results = game.play_game()
            for name, points in results.items():
                self.stats[name] += points
                
        # Sort stats by extracting player number from player names and convert it to an integer for sorting
        sorted_stats = dict(sorted(self.stats.items(), key=lambda item: int(item[0].split(' ')[1])))
        
        # Print sorted statistics
        # for name, total_points in sorted_stats.items():
        #     print(f"{name}: {total_points} points over {self.num_games} games")
        
        return sorted_stats

if __name__ == "__main__":
    # Example usage
    player_strategies = ["random", "smart_random", "position_search", "color_search","Colton_special"]  # Example strategies
    simulation = Simulation(10000, player_strategies)
    results = simulation.run()
    for name, points in results.items():
        print(f"{name}: {points} points over {simulation.num_games} games")