import pandas as pd

# Load datasets
results_2014 = pd.read_csv("constituency_wise_results_2014.csv")
results_2019 = pd.read_csv("constituency_wise_results_2019.csv")
state_codes = pd.read_csv("dim_states_codes.csv")

# Merge state codes to results datasets
results_2014 = pd.merge(results_2014, state_codes, left_on='state', right_on='state_name', how='left')
results_2019 = pd.merge(results_2019, state_codes, left_on='state', right_on='state_name', how='left')

# Open or create a new file named "Answers.txt" in write mode
with open("Answers.txt", "w") as f:
    # Question 1: List top 5/bottom 5 constituencies of 2014 and 2019 in terms of voter turnout ratio
    results_2014['Turnout_Ratio_2014'] = results_2014['total_votes'] / results_2014['total_electors']
    results_2019['Turnout_Ratio_2019'] = results_2019['total_votes'] / results_2019['total_electors']

    top_bottom_turnout_2014 = pd.concat([results_2014.sort_values(by='Turnout_Ratio_2014', ascending=False).head(),
                                         results_2014.sort_values(by='Turnout_Ratio_2014').head()])
    top_bottom_turnout_2019 = pd.concat([results_2019.sort_values(by='Turnout_Ratio_2019', ascending=False).head(),
                                         results_2019.sort_values(by='Turnout_Ratio_2019').head()])

    f.write("Question 1: List top 5/bottom 5 constituencies of 2014 and 2019 in terms of voter turnout ratio\n\n")
    f.write("Top 5 constituencies with highest voter turnout ratio in 2014:\n")
    f.write(str(top_bottom_turnout_2014.head()) + "\n\n")
    f.write("Bottom 5 constituencies with lowest voter turnout ratio in 2014:\n")
    f.write(str(top_bottom_turnout_2014.tail()) + "\n\n")
    f.write("Top 5 constituencies with highest voter turnout ratio in 2019:\n")
    f.write(str(top_bottom_turnout_2019.head()) + "\n\n")
    f.write("Bottom 5 constituencies with lowest voter turnout ratio in 2019:\n")
    f.write(str(top_bottom_turnout_2019.tail()) + "\n\n")

    # Question 2: List top 5/bottom 5 states of 2014 and 2019 in terms of voter turnout ratio
    state_turnout_2014 = results_2014.groupby('abbreviation')['Turnout_Ratio_2014'].mean().sort_values(ascending=False).head()
    state_turnout_2019 = results_2019.groupby('abbreviation')['Turnout_Ratio_2019'].mean().sort_values(ascending=False).head()

    f.write("Question 2: List top 5/bottom 5 states of 2014 and 2019 in terms of voter turnout ratio\n\n")
    f.write("Top 5 states with highest voter turnout ratio in 2014:\n")
    f.write(str(state_turnout_2014.head()) + "\n\n")
    f.write("Bottom 5 states with lowest voter turnout ratio in 2014:\n")
    f.write(str(state_turnout_2014.tail()) + "\n\n")
    f.write("Top 5 states with highest voter turnout ratio in 2019:\n")
    f.write(str(state_turnout_2019.head()) + "\n\n")
    f.write("Bottom 5 states with lowest voter turnout ratio in 2019:\n")
    f.write(str(state_turnout_2019.tail()) + "\n\n")

    # Question 3: Which constituencies have elected the same party for two consecutive elections, rank them by % of votes to that winning party in 2019
    consecutive_party = results_2014.merge(results_2019, on=['state', 'pc_name'])
    consecutive_party = consecutive_party[(consecutive_party['party_x'] == consecutive_party['party_y']) & 
                                          (consecutive_party['party_symbol_x'] == consecutive_party['party_symbol_y'])]
    consecutive_party_ranked = consecutive_party.sort_values(by='general_votes_y', ascending=False)

    f.write("Question 3: Which constituencies have elected the same party for two consecutive elections, rank them by % of votes to that winning party in 2019\n\n")
    f.write("Constituencies that have elected the same party for two consecutive elections, ranked by % of votes to the winning party in 2019:\n")
    f.write(str(consecutive_party_ranked.head()) + "\n\n")

    # Question 4: Which constituencies have voted for different parties in two elections (list top 10 based on difference (2019-2014) in winner vote percentage in two elections)
    different_party = results_2014.merge(results_2019, on=['state', 'pc_name'])
    different_party = different_party[(different_party['party_x'] != different_party['party_y'])]
    different_party['Vote_Percentage_Difference'] = different_party['general_votes_y'] - different_party['general_votes_x']
    top_different_party = different_party.sort_values(by='Vote_Percentage_Difference', ascending=False).head(10)

    f.write("Question 4: Which constituencies have voted for different parties in two elections (list top 10 based on difference (2019-2014) in winner vote percentage in two elections)\n\n")
    f.write("Top 10 constituencies that have voted for different parties in two elections, based on the difference in winner vote percentage in 2019 compared to 2014:\n")
    f.write(str(top_different_party.head()) + "\n\n")

    # Question 5: Top 5 candidates based on margin difference with runners in 2014 and 2019
    top_margin_2014 = results_2014.sort_values(by='general_votes', ascending=False).head()
    top_margin_2019 = results_2019.sort_values(by='general_votes', ascending=False).head()

    f.write("Question 5: Top 5 candidates based on margin difference with runners in 2014 and 2019\n\n")
    f.write("Top 5 candidates with the highest margin difference with runners in 2014:\n")
    f.write(str(top_margin_2014) + "\n\n")
    f.write("Top 5 candidates with the highest margin difference with runners in 2019:\n")
    f.write(str(top_margin_2019) + "\n\n")

    # Question 6: % Split of votes of parties between 2014 vs 2019 at national level
    party_votes_2014 = results_2014.groupby('party')['general_votes'].sum()
    party_votes_2019 = results_2019.groupby('party')['general_votes'].sum()
    party_votes_split_national = (party_votes_2019 - party_votes_2014) / party_votes_2014 * 100

    f.write("Question 6: % Split of votes of parties between 2014 vs 2019 at national level\n\n")
    f.write("Percentage split of votes of parties between 2014 and 2019 at national level:\n")
    f.write(str(party_votes_split_national) + "\n\n")

    # Question 7: % Split of votes of parties between 2014 vs 2019 at state level
    party_votes_2014_state = results_2014.groupby(['abbreviation', 'party'])['general_votes'].sum()
    party_votes_2019_state = results_2019.groupby(['abbreviation', 'party'])['general_votes'].sum()
    party_votes_split_state = (party_votes_2019_state - party_votes_2014_state) / party_votes_2014_state * 100

    f.write("Question 7: % Split of votes of parties between 2014 vs 2019 at state level\n\n")
    f.write("Percentage split of votes of parties between 2014 and 2019 at state level:\n")
    f.write(str(party_votes_split_state) + "\n\n")

    # Question 8: List top 5 constituencies for two major national parties where they have gained vote share in 2019 as compared to 2014
    major_parties_gain = results_2014.merge(results_2019, on=['state', 'pc_name'])
    major_parties_gain = major_parties_gain[(major_parties_gain['party_x'].isin(['TDP', 'BJP'])) & 
                                            (major_parties_gain['party_y'].isin(['TDP', 'BJP'])) & 
                                            (major_parties_gain['general_votes_y'] > major_parties_gain['general_votes_x'])].head()

    f.write("Question 8: List top 5 constituencies for two major national parties where they have gained vote share in 2019 as compared to 2014\n\n")
    f.write("Top 5 constituencies for two major national parties where they have gained vote share in 2019 compared to 2014:\n")
    f.write(str(major_parties_gain.head()) + "\n\n")

    # Question 9: List top 5 constituencies for two major national parties where they have lost vote share in 2019 as compared to 2014
    major_parties_loss = results_2014.merge(results_2019, on=['state', 'pc_name'])
    major_parties_loss = major_parties_loss[(major_parties_loss['party_x'].isin(['TDP', 'BJP'])) & 
                                            (major_parties_loss['party_y'].isin(['TDP', 'BJP'])) & 
                                            (major_parties_loss['general_votes_y'] < major_parties_loss['general_votes_x'])].head()

    f.write("Question 9: List top 5 constituencies for two major national parties where they have lost vote share in 2019 as compared to 2014\n\n")
    f.write("Top 5 constituencies for two major national parties where they have lost vote share in 2019 compared to 2014:\n")
    f.write(str(major_parties_loss.head()) + "\n\n")

    # Question 10: Which constituency has voted the most for NOTA?
    most_nota_constituency = results_2019.sort_values(by='general_votes', ascending=False).head(1)

    f.write("Question 10: Which constituency has voted the most for NOTA?\n\n")
    f.write("Constituency that has voted the most for NOTA:\n")
    f.write(str(most_nota_constituency) + "\n\n")
