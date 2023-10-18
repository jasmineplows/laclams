import streamlit as st
import pandas as pd

# Function to load data
@st.cache_data
def load_data():
    return pd.read_csv('team_stats.csv')

# Function to format the numbers in the DataFrame
def format_float(val):
    if isinstance(val, float):
        return f"{val:.1f}"
    return val  # Non-floats are returned as-is

def main():

    st.set_page_config(
        page_title="LA Clams Stats",
        page_icon="🏈"
    )

    hide_menu_style = """
    <style>
    #MainMenu {visability: hidden;}
    footer {visibility: hidden;}
    </style>
    """

    st.markdown(hide_menu_style, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.1,0.1,0.1])

    with col1:
        st.write("")

    with col2:
        st.image("logo.png")

    with col3:
        st.write("")

    st.title("LA Clams Statistics")

    # Load data
    data = load_data()

    st.subheader("🍁 Fall 2023 Season 🍁")
    
    # First, ensure we only include weeks with data
    weeks_with_data = data['Week'].unique()

    # Initialize variables to store total stats
    total_clams_points = 0
    total_opponent_points = 0
    total_plays = 0
    total_offensive_plays = 0
    total_defensive_plays = 0
    total_passing_tds = 0
    total_rushing_tds = 0
    total_interceptions_offense = 0
    total_interceptions_defense = 0
    total_rushing_yards = 0
    total_receiving_yards = 0
    total_tds = 0
    total_flags_pulled = 0
    successful_conversions = 0
    attempted_conversions = 0
    total_penalties = 0

    # Calculate statistics for each week and accumulate totals
    for week in weeks_with_data:
        week_data = data[data['Week'] == week]

        # Calculate statistics
        clams_points_scored = week_data[(week_data['Offense/Defense'] == 'Offense') & (week_data['Action'] != 'Pick-Six')]['Points'].sum()
        opponent_points_scored = week_data[(week_data['Offense/Defense'] == 'Defense') | ((week_data['Offense/Defense'] == 'Offense') & (week_data['Action'] == 'Pick-Six'))]['Points'].sum()
        plays = len(week_data)
        offensive_plays = len(week_data[week_data['Offense/Defense'] == 'Offense'])
        defensive_plays = len(week_data[week_data['Offense/Defense'] == 'Defense'])
        passing_tds = len(week_data[(week_data['Offense/Defense'] == 'Offense') & (week_data['Action'] == 'Touchdown') & (week_data['Touchdown Type'] == 'Passing Touchdown')])
        rushing_tds = len(week_data[(week_data['Offense/Defense'] == 'Offense') & (week_data['Action'] == 'Touchdown') & (week_data['Touchdown Type'] == 'Rushing Touchdown')])
        interceptions_offense = len(week_data[(week_data['Offense/Defense'] == 'Offense') & week_data['Action'].isin(['Interception', 'Pick-Six'])])
        interceptions_defense = len(week_data[(week_data['Offense/Defense'] == 'Defense') & week_data['Action'].isin(['Interception', 'Pick-Six'])])
        rushing_yards = week_data[(week_data['Offense/Defense'] == 'Offense') & (week_data['Touchdown Type'] == 'Rushing Touchdown')]['Yards'].sum()
        receiving_yards = week_data[(week_data['Offense/Defense'] == 'Offense') & (week_data['Touchdown Type'] == 'Passing Touchdown')]['Yards'].sum()
        total_tds_game = passing_tds + rushing_tds
        flags_pulled = len(week_data[week_data['Action'] == 'Flag Pull'])
        conversions_made = len(week_data[(week_data['Offense/Defense'] == 'Offense') & (week_data['Conversion Outcome'] == 'Complete')])
        conversions_attempted = len(week_data[(week_data['Offense/Defense'] == 'Offense') & (week_data['Action'] == 'Conversion')])
        penalties = len(week_data[week_data['Action'] == 'Penalty'])

        # Accumulate totals
        total_clams_points += clams_points_scored
        total_opponent_points += opponent_points_scored
        total_plays += plays
        total_offensive_plays += offensive_plays
        total_defensive_plays += defensive_plays
        total_passing_tds += passing_tds  # assuming you calculate this per game
        total_rushing_tds += rushing_tds  # assuming you calculate this per game
        total_interceptions_offense += interceptions_offense  # assuming you calculate this per game
        total_interceptions_defense += interceptions_defense  # assuming you calculate this per game
        total_rushing_yards += rushing_yards  # assuming you calculate this per game
        total_receiving_yards += receiving_yards  # assuming you calculate this per game
        total_tds += total_tds_game  # assuming you calculate total touchdowns per game
        total_flags_pulled += flags_pulled  # assuming you calculate this per game
        successful_conversions += conversions_made  # assuming you calculate this per game
        attempted_conversions += conversions_attempted  # assuming you calculate this per game
        total_penalties += penalties  # assuming you calculate this per game

    # Now, calculate the average statistics over the season
    num_games= len(weeks_with_data)
    avg_clams_points = round(total_clams_points / num_games, 1)
    avg_opponent_points = round(total_opponent_points / num_games, 1)
    avg_plays = round(total_plays / num_games, 1)
    avg_offensive_plays = round(total_offensive_plays / num_games, 1)
    avg_defensive_plays = round(total_defensive_plays / num_games, 1)
    avg_passing_tds = round(total_passing_tds / num_games, 1)
    avg_rushing_tds = round(total_rushing_tds / num_games, 1)
    avg_interceptions_offense = round(total_interceptions_offense / num_games, 1)
    avg_interceptions_defense = round(total_interceptions_defense / num_games, 1)
    avg_rushing_yards = round(total_rushing_yards / num_games, 1)
    avg_receiving_yards = round(total_receiving_yards / num_games, 1)
    avg_total_tds = round(total_tds / num_games, 1)
    avg_flags_pulled = round(total_flags_pulled / num_games, 1)
    avg_successful_conversions = round(successful_conversions / num_games, 1)
    avg_attempted_conversions = round(attempted_conversions / num_games, 1)
    avg_conversion_rate = round((avg_successful_conversions / avg_attempted_conversions) * 100 if avg_attempted_conversions > 0 else 0, 1)
    avg_penalties = round(total_penalties / num_games, 1)

    # Create a summary dictionary for the season averages
    season_averages_summary = {
        'Games Played (w/stats)': num_games,
        'Average LA Clams Points per Game': f"{avg_clams_points:.1f}",
        'Average Opponent Points per Game': f"{avg_opponent_points:.1f}",
        'Average Total Plays per Game': f"{avg_plays:.1f}",
        'Average Offensive Plays per Game': f"{avg_offensive_plays:.1f}",
        'Average Defensive Plays per Game': f"{avg_defensive_plays:.1f}",
        'Average Passing TDs per Game': f"{avg_passing_tds:.1f}",
        'Average Rushing TDs per Game': f"{avg_rushing_tds:.1f}",
        'Average Interceptions (while on Offense) per Game': f"{avg_interceptions_offense:.1f}",
        'Average Interceptions (while on Defense) per Game': f"{avg_interceptions_defense:.1f}",
        'Average Rushing Yards per Game': f"{avg_rushing_yards:.1f}",
        'Average Receiving Yards per Game': f"{avg_receiving_yards:.1f}",
        'Average Total TDs per Game': f"{avg_total_tds:.1f}",
        'Average Flags Pulled per Game': f"{avg_flags_pulled:.1f}",
        'Average Successful Conversions per Game': f"{avg_successful_conversions:.1f}",
        'Average Attempted Conversions per Game': f"{avg_attempted_conversions:.1f}",
        'Average Conversion Rate (%)': f"{avg_conversion_rate:.1f}",
        'Average Penalties per Game': f"{avg_penalties:.1f}",
}

    # Display the season average summary
    st.subheader('Season Averages')
    # Apply the formatting function to the DataFrame before displaying it
    season_averages_summary_df = pd.DataFrame([season_averages_summary]).applymap(format_float)
    season_averages_summary_df = season_averages_summary_df.transpose().reset_index()
    season_averages_summary_df.columns = ["Statistic", "Value"]
    st.table(season_averages_summary_df)

    st.subheader("Individual Game Statistics")

    all_weeks = ['Week ' + str(i) for i in range(1, 11)]  # for weeks 1 through 10

    # Create a dropdown to select the Week
    week_selection = st.selectbox('Select a Week', all_weeks)

    # Extracting the week number from the selection
    week_number = int(week_selection.split(' ')[1])  # Converts 'Week 2' to 2, for example

    if week_number not in data['Week'].unique():
        # If the selected week is not in the dataset, display an error message
        st.error(f"Unfortunately, no stats were captured for {week_selection}. Alternatively, the week you have selected is in the future. Please select another week.")
    else:
        # Filter data for the selected Week
        week_data = data[data['Week'] == week_number]

        # Calculate the various statistics
        opponent = week_data['Opponent'].iloc[0]
        clams_points_scored = week_data[(week_data['Offense/Defense'] == 'Offense') & (week_data['Action'] != 'Pick-Six')]['Points'].sum()
        total_points_allowed = week_data[(week_data['Offense/Defense'] == 'Defense') | ((week_data['Offense/Defense'] == 'Offense') & (week_data['Action'] == 'Pick-Six'))]['Points'].sum()
        outcome = "W" if clams_points_scored > total_points_allowed else "L"
        num_plays = len(week_data)
        num_offense_plays = len(week_data[week_data['Offense/Defense'] == 'Offense'])
        num_defense_plays = len(week_data[week_data['Offense/Defense'] == 'Defense'])
        percent_plays_offense = (num_offense_plays / num_plays) * 100 if num_plays > 0 else 0
        percent_plays_defense = (num_defense_plays / num_plays) * 100 if num_plays > 0 else 0
        successful_offense = len(week_data[week_data['Offense/Defense'] == 'Offense'][week_data['Yards'] > 0])
        pct_successful_offense = (successful_offense/num_offense_plays) * 100 if num_offense_plays > 0 else 0
        successful_defense = len(week_data[week_data['Offense/Defense'] == 'Defense'][week_data['Yards'] <= 0])
        pct_successful_defense = (successful_defense/num_defense_plays) * 100 if num_defense_plays > 0 else 0
        passing_tds = len(week_data[week_data['Offense/Defense'] == 'Offense'][week_data['Action'] == 'Touchdown'][week_data['Touchdown Type'] == 'Passing Touchdown'])
        rushing_tds = len(week_data[week_data['Offense/Defense'] == 'Offense'][week_data['Action'] == 'Touchdown'][week_data['Touchdown Type'] == 'Rushing Touchdown'])
        interceptions_offense = len(week_data[(week_data['Offense/Defense'] == 'Offense') & week_data['Action'].isin(['Interception', 'Pick-Six'])])
        interceptions_defense = len(week_data[(week_data['Offense/Defense'] == 'Defense') & week_data['Action'].isin(['Interception', 'Pick-Six'])])
        total_rushing_yards = week_data[week_data['Offense/Defense'] == 'Offense'][week_data['Touchdown Type'] == 'Rushing Touchdown']['Yards'].sum()
        total_receiving_yards = week_data[week_data['Offense/Defense'] == 'Offense'][week_data['Touchdown Type'] == 'Passing Touchdown']['Yards'].sum()
        total_tds = passing_tds + rushing_tds
        total_flags_pulled = len(week_data[week_data['Action'] == 'Flag Pull'])
        successful_conversions = len(week_data[week_data['Offense/Defense'] == 'Offense'][week_data['Conversion Outcome'] == 'Complete'])
        attempted_conversions = len(week_data[week_data['Offense/Defense'] == 'Offense'][week_data['Action'] == 'Conversion'])
        conversion_rate = (successful_conversions / attempted_conversions) * 100 if attempted_conversions > 0 else 0
        total_penalties = len(week_data[week_data['Action'] == 'Penalty'])

        # Create a dictionary for the summary
        summary = {
            'Week': week_number,
            'Opponent Name': opponent,
            'Outcome': outcome,
            'LA Clams Score': clams_points_scored,
            'Opponent Score': total_points_allowed,
            'Total Plays': num_plays,
            'Total Offensive Plays': num_offense_plays,
            'Total Defensive Plays': num_defense_plays,
            '% Plays on Offense': percent_plays_offense,
            'Successful Offensive Plays': successful_offense,
            '% Successful Offensive Plays': pct_successful_offense,
            'Successful Defensive Stops': successful_defense,
            '% Successful Defensive Stops': pct_successful_defense,
            'Passing TDs': passing_tds,
            'Rushing TDs': rushing_tds,
            'Int (while on offense)': interceptions_offense,
            'Int (while on defense)': interceptions_defense,
            'Total Rushing Yards': total_rushing_yards,
            'Total Receiving Yards': total_receiving_yards,
            'Total TDs': total_tds,
            'Total Flags Pulled': total_flags_pulled,
            'Successful Conversions': successful_conversions,
            'Attempted Conversions': attempted_conversions,
            'Conversion Rate': conversion_rate,
            'Total Penalties': total_penalties,
        }


        # Display the summary as a table
        df = pd.DataFrame([summary])

        df.index = range(1, len(df) + 1)

        # Transpose the dataframe and reset its index for display
        transposed_df = df.head(1).transpose().reset_index()
        transposed_df.columns = ["Statistic", "Value"]

        transposed_df['Value'] = transposed_df['Value'].apply(lambda x: round(x, 1) if isinstance(x, float) else x)

        st.table(transposed_df)

if __name__ == "__main__":
    main()