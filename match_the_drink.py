import streamlit as st
from game_engine import Simulation, Player

# Available strategies for the dropdown
AVAILABLE_STRATEGIES = ["random", "smart_random", "search_by_color", "search_by_position", "sequential"]

# Game colors and positions from game engine
GAME_COLORS = ["red", "blue", "green", "yellow", "orange", "purple"]
GAME_POSITIONS = list(range(1, 7))

def display_game_board():
    """Display a visual representation of the game board"""
    st.markdown("### 🎯 Game Board Concept")
    
    # Create a simple visual representation
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Colors:**")
        for color in GAME_COLORS:
            # Create colored square emoji/text
            if color == "red":
                st.markdown(f"🔴 {color.capitalize()}")
            elif color == "blue":
                st.markdown(f"🔵 {color.capitalize()}")
            elif color == "green":
                st.markdown(f"🟢 {color.capitalize()}")
            elif color == "yellow":
                st.markdown(f"🟡 {color.capitalize()}")
            elif color == "orange":
                st.markdown(f"🟠 {color.capitalize()}")
            elif color == "purple":
                st.markdown(f"🟣 {color.capitalize()}")
    
    with col2:
        
        st.markdown("**Example Layout:**")
        st.markdown("```\nColors 🔵 🟢 🟡 🔴 🟠 🟣\n\nPositions: 1 2 3 4 5 6\n```")
    
    st.info("💡 **How it works**: Each color is secretly assigned to one position. Players guess combinations to find the correct matches!")

st.title("Match the Drink Game Simulator")

# Display the game board visualization at the top
display_game_board()
st.markdown("---")

st.sidebar.header("Game Configuration")

# Number of games to simulate
num_games = st.sidebar.slider("Number of Games", min_value=1, max_value=10000, value=100, step=10)

# Number of players
num_players = st.sidebar.slider("Number of Players", min_value=1, max_value=6, value=4)

st.header("Player Configuration")

# Dynamic player configuration
players = []
player_names = []

for i in range(num_players):
    st.subheader(f"Player {i+1}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        player_name = st.text_input(f"Player {i+1} Name", value=f"Player {i+1}", key=f"name_{i}")
    
    with col2:
        strategy = st.selectbox(
            f"Strategy",
            AVAILABLE_STRATEGIES,
            index=i % len(AVAILABLE_STRATEGIES),
            key=f"strategy_{i}"
        )
    
    # Add custom order options for systematic and sequential strategies
    if strategy in ["search_by_color", "search_by_position", "sequential"]:
        with st.expander(f"🎛️ Custom Order for {player_name}", expanded=False):
            col_a, col_b = st.columns(2)
            
            with col_a:
                # Color order selection
                st.markdown("**Color Order:**")
                color_order = st.multiselect(
                    f"Select color order",
                    GAME_COLORS,
                    default=GAME_COLORS,
                    key=f"color_order_{i}",
                    help="Drag to reorder the colors for systematic search"
                )
                
                # Display current order
                if color_order:
                    st.markdown("**Current Order:**")
                    order_display = " → ".join([f"🔴" if c == "red" else f"🔵" if c == "blue" else f"🟢" if c == "green" else f"🟡" if c == "yellow" else f"🟠" if c == "orange" else f"🟣" for c in color_order])
                    st.markdown(order_display)
            
            with col_b:
                # Position order selection
                st.markdown("**Position Order:**")
                position_order = st.multiselect(
                    f"Select position order",
                    GAME_POSITIONS,
                    default=GAME_POSITIONS,
                    key=f"position_order_{i}",
                    help="Drag to reorder the positions for systematic search"
                )
                
                # Display current order
                if position_order:
                    st.markdown("**Current Order:**")
                    st.markdown(" → ".join([f"#{p}" for p in position_order]))
    else:
        color_order = None
        position_order = None
    
    # Check for duplicate names
    if player_name in player_names:
        st.error(f"Duplicate player name: {player_name}. Please choose unique names.")
    
    player_names.append(player_name)
    players.append((player_name, strategy, color_order, position_order))

# Run simulation button
if st.button("🎯 Run Simulation", type="primary"):
    # Validate no duplicate names
    if len(set(player_names)) != len(player_names):
        st.error("Please ensure all player names are unique.")
    else:
        # Create Player objects
        player_objects = []
        for name, strategy, color_order, position_order in players:
            # Convert to proper lists if provided, otherwise use defaults
            final_color_order = color_order if color_order else None
            final_position_order = position_order if position_order else None
            
            player_objects.append(Player(strategy, name, final_color_order, final_position_order))
        
        # Run simulation
        simulation = Simulation(num_games, player_objects)
        
        with st.spinner("Running simulation..."):
            results = simulation.run()
        
        # Display results
        st.success("Simulation Complete!")
        
        st.header("📊 Results")
        
        # Create a nice table
        import pandas as pd
        
        df = pd.DataFrame({
            'Player': list(results.keys()),
            'Total Points': list(results.values()),
            'Average Points per Game': [round(points/num_games, 2) for points in results.values()],
            'Win Rate': [f"{round(points/(num_games*6)*100, 1)}%" for points in results.values()]  # Assuming 6 points max per game
        })
        
        st.dataframe(df, use_container_width=True)
        
        # Create a bar chart
        st.subheader("📈 Points Distribution")
        st.bar_chart(df.set_index('Player')['Total Points'])
        
        # Additional statistics
        st.subheader("📈 Additional Statistics")
        total_points = sum(results.values())
        max_points = max(results.values())
        winner = max(results.items(), key=lambda x: x[1])[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Points Scored", total_points)
        with col2:
            st.metric("Highest Scoring Player", winner)
        with col3:
            st.metric("Max Points", f"{max_points} ({round(max_points/num_games, 2)} per game)")

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    1. **Configure Game**: Use the sidebar to set the number of games and players
     2. **Set Up Players**: For each player, enter a unique name and select a strategy:
        - **random**: Randomly chooses color and position
        - **smart_random**: Avoids repeating previous guesses
        - **search_by_color**: Picks one color and searches all positions
        - **search_by_position**: Picks one position and searches all colors
        - **sequential**: Advances both color and position indices together (e.g., blue 1, green 2, yellow 3...)
    3. **Run Simulation**: Click the button to run the simulation
    4. **View Results**: See detailed statistics and visualizations
    
     **Strategies Explained:**
     - *search_by_color*: Systematically tests one color across all positions (e.g., blue 1, blue 2, blue 3...)
     - *search_by_position*: Systematically tests one position across all colors (e.g., red 1, blue 1, green 1...)
     - *sequential*: Advances both color and position indices simultaneously (e.g., blue 1, green 2, yellow 3...)
     
     **Custom Orders:**
     - Only available for systematic and sequential strategies
     - **Color Order**: Choose which colors to test first (e.g., test 🔴 red before 🔵 blue)
     - **Position Order**: Choose which positions to test first (e.g., test #1 before #6)
     - **Strategic Impact**: Custom orders can significantly affect performance based on your game theory!
    """)

# Footer
st.markdown("---")
st.markdown("💡 **Tip**: Try different strategy combinations to see which performs best!")