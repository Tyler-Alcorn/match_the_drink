import random
from collections import defaultdict

class Player:
    def __init__(self, strategy, name, color_order=None, position_order=None):
        self.strategy = strategy
        self.name = name
        # Initialize for strategies requiring predefined orders or indices
        # Allow custom orders to be passed in, defaulting to a predefined order if not specified
        self.position_order = position_order if position_order else [1, 2, 3, 4, 5, 6]
        self.color_order = color_order if color_order else ["red", "blue", "green", "yellow", "orange", "purple"]
        self.reset_for_new_game()
        # Track the last guess to determine the next step
        # self.last_position_index = -1  # Tracks the last position guessed
        # self.last_color_index = -1  # Tracks the last color guessed
    
    def add_point(self):
        self.points += 1

    def guess(self, remaining_colors, remaining_positions):
        # Implement different guessing strategies
        # pick a random color and position from the remaining ones
        if self.strategy == "random":
            return random.choice(remaining_colors), random.choice(remaining_positions)
        
#stragety sequential, where player goes through colors and positions in order at the same time for example blue 1, green 2, yellow 3, orange 4
        elif self.strategy == "sequential": 
            # Simple approach: advance both indices, skip unavailable items
            if not remaining_colors or not remaining_positions:
                return None, None
            
            # Find next available color
            for _ in range(len(self.color_order)):
                current_color = self.color_order[self.color_index]
                if current_color in remaining_colors:
                    break
                self.color_index = (self.color_index + 1) % len(self.color_order)
            else:
                return None, None
            
            # Find next available position
            for _ in range(len(self.position_order)):
                current_position = self.position_order[self.position_index]
                if current_position in remaining_positions:
                    break
                self.position_index = (self.position_index + 1) % len(self.position_order)
            else:
                return None, None
            
            # Advance both for next time
            self.color_index = (self.color_index + 1) % len(self.color_order)
            self.position_index = (self.position_index + 1) % len(self.position_order)
            
            return current_color, current_position
        
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
            
        elif self.strategy == "search_by_position" or self.strategy == "search_by_color":
            guess = self.__systematic_search_guess(remaining_colors, remaining_positions)
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
        self.current_color_index = 0  # Reset for search_by_color
        self.current_position_index = 0  # Reset for search_by_position

    def __systematic_search_guess(self, remaining_colors, remaining_positions):
        if self.strategy == "search_by_color":
            # Simple approach: find first available color, iterate through positions
            if not remaining_colors or not remaining_positions:
                return None, None
                
            # Find current available color
            while self.last_color_index < len(self.color_order):
                current_color = self.color_order[self.last_color_index]
                if current_color in remaining_colors:
                    break
                self.last_color_index += 1
            else:
                # Wrap around to start
                self.last_color_index = 0
                while self.last_color_index < len(self.color_order):
                    current_color = self.color_order[self.last_color_index]
                    if current_color in remaining_colors:
                        break
                    self.last_color_index += 1
                else:
                    return None, None
            
            # Find first available position for this color
            self.last_position_index = (self.last_position_index + 1) % len(self.position_order)
            for _ in range(len(self.position_order)):
                selected_position = self.position_order[self.last_position_index]
                if selected_position in remaining_positions:
                    return current_color, selected_position
                self.last_position_index = (self.last_position_index + 1) % len(self.position_order)
            
            return None, None
        
        elif self.strategy == "search_by_position":
            # Simple approach: find first available position, iterate through colors
            if not remaining_colors or not remaining_positions:
                return None, None
                
            # Find current available position
            while self.last_position_index < len(self.position_order):
                current_position = self.position_order[self.last_position_index]
                if current_position in remaining_positions:
                    break
                self.last_position_index += 1
            else:
                # Wrap around to start
                self.last_position_index = 0
                while self.last_position_index < len(self.position_order):
                    current_position = self.position_order[self.last_position_index]
                    if current_position in remaining_positions:
                        break
                    self.last_position_index += 1
                else:
                    return None, None
            
            # Find first available color for this position
            self.last_color_index = (self.last_color_index + 1) % len(self.color_order)
            for _ in range(len(self.color_order)):
                selected_color = self.color_order[self.last_color_index]
                if selected_color in remaining_colors:
                    return selected_color, current_position
                self.last_color_index = (self.last_color_index + 1) % len(self.color_order)
            
            return None, None
    
class Game:
    def __init__(self, players):
        self.players = players
        self.colors = [
            "red", "blue", "green", "yellow", "orange",
            "purple"]
        self.positions = list(range(1, 7))  # Positions 1 through 6
        self.correct_assignments = {}
        self.round_order = []
        self.__initialize_game()
    
    def __initialize_game(self):
        random.shuffle(self.colors)
        for position, color in zip(self.positions, self.colors):
            self.correct_assignments[position] = color
        # Initialize the order for the first round
        self.round_order = self.players.copy()
        random.shuffle(self.round_order)
        random.shuffle(self.colors)

    def _play_round(self):

        for player in self.round_order:
            guess_color, guess_position = player.guess(self.colors, self.positions)
            #if self.correct_assignments.get(guess_position) == guess_color:
            if self.correct_assignments[guess_position] == guess_color:
                player.add_point()
                self.colors.remove(guess_color)
                self.positions.remove(guess_position)
                if len(self.colors) == 0:  # Last drink guessed correctly
                    return True  # Game over
        return False  # Game continues
    
    def play_game(self):
        while not self._play_round():
            pass
        game_results = {player.name: player.points for player in self.players}
        # Reset for next game
        for player in self.players:
            player.reset_for_new_game()  # Corrected to call the right method
        self.colors = [
            "red", "blue", "green", "yellow", "orange",
            "purple"]
        self.positions = list(range(1, 7))
        self.__initialize_game()
        return game_results
  
class Simulation:
    def __init__(self, num_games, players):
        self.num_games = num_games
        self.players = players
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
                
        # Sort stats alphabetically by player name since we now support custom names
        sorted_stats = dict(sorted(self.stats.items()))
        
        # Print sorted statistics
        # for name, total_points in sorted_stats.items():
        #     print(f"{name}: {total_points} points over {self.num_games} games")
        
        return sorted_stats

if __name__ == "__main__":
    # Example usage
    # Initialize Players with custom orders
    players = [
        Player("search_by_position", "Player 1"),
        Player("random", "Player 2"),
        Player("random", "Player 3"),
        Player("smart_random", "Player 4"),
        Player("search_by_color", "Player 5", position_order=[6, 5, 4, 3, 2, 1])
    ]
    
    # Create and run the Simulation
    simulation = Simulation(100, players)
    results = simulation.run()
    for name, points in results.items():
        print(f"{name}: {points} points over {simulation.num_games} games")