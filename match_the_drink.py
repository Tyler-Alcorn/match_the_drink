# import gradio as gr
# from game_engine import Simulation  # Import the Simulation class from game_engine.py

# def run_simulation(num_games, players):
#     # Split the comma-separated string of strategies into a list
#     #player_strategies_list = player_strategies
#     # Initialize the simulation with the provided number of games and strategies
#     simulation = Simulation(num_games, players)
#     # Run the simulation
#     results = simulation.run()
#     # Format the results for display
#     result_str = "\n".join([f"{name}: {points} points" for name, points in results.items()])
    
#     return result_str

# # Setup the Gradio interface
# iface = gr.Interface(
#     fn=run_simulation,
#     inputs=[
#         gr.Radio([1, 100, 1000, 10000], label="Number of games to Run"),
#         #gr.Textbox(label="Player Strategies (comma-separated)", value="Colton_special, position_search, color_search"),
#         gr.Dropdown(["random", "smart_random", "position_search", "color_search", "Colton_special"], value=["position_search", "color_search", "Colton_special"], multiselect=True, label="Player strategy", info=""),
#     ],
#     outputs=gr.Textbox(label="Results"),
#     title="Game Simulation",
#     description="Enter the number of games and player strategies to simulate."
# )

# # Launch the Gradio app
# if __name__ == "__main__":
#     iface.launch(share=True)



import gradio as gr

def run_simulation(num_games, num_players, *player_details):
    # Filter out empty player details based on num_players
    player_details = player_details[:int(num_players)]  # Ensure num_players is an int and use it to slice the player_details
    
    # Now, player_details will only contain the inputs for the number of players specified by num_players
    # Process player_details as needed for your application
    # Example: Assuming player_details format: "Name,Strategy"
    processed_players = [detail.split(',') for detail in player_details if detail]  # Simple processing
    
    # Example processing of processed_players
    for name, strategy in processed_players:
        print(f"Player Name: {name}, Strategy: {strategy}")
    
    # Placeholder for actual simulation logic
    return f"Simulated {num_games} games for {num_players} players."

# Define inputs including a slider for the number of players and text inputs for player details
inputs = [
    gr.Slider(minimum=1, maximum=5, label="Number of Games to Run", value=1),
    gr.Slider(minimum=1, maximum=5, label="Number of Players", value=2),
]

# Generate text inputs for player details
for i in range(1, 6):  # Assuming a maximum of 5 players for this example
    inputs.append(gr.Textbox(label=f"Player {i} Details (Name,Strategy)", ))

iface = gr.Interface(
    fn=run_simulation,
    inputs=inputs,
    outputs=gr.Textbox(label="Results"),
    title="Game Simulation",
    description="Use the slider to select the number of players, then enter details for each player."
)

iface.launch()