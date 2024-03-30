import gradio as gr
from game_engine import Simulation  # Import the Simulation class from game_engine.py

def run_simulation(num_games, player_strategies):
    # Split the comma-separated string of strategies into a list
    player_strategies_list = [strategy.strip() for strategy in player_strategies.split(",")]
    # Initialize the simulation with the provided number of games and strategies
    simulation = Simulation(num_games, player_strategies_list)
    # Run the simulation
    results = simulation.run()
    # Format the results for display
    result_str = "\n".join([f"{name}: {points} points" for name, points in results.items()])
    return result_str

# Setup the Gradio interface
iface = gr.Interface(
    fn=run_simulation,
    inputs=[
        gr.Number(label="Number of Games", value=100),
        gr.Textbox(label="Player Strategies (comma-separated)", value="Colton_special, position_search, color_search")
    ],
    outputs=gr.Textbox(label="Results"),
    title="Game Simulation",
    description="Enter the number of games and player strategies to simulate."
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch(share=True)
