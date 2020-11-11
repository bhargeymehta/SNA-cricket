import yaml

def extract_and_dump(filename, partnership_prefix, wickets_prefix, performance_prefix, innings_prefix):
    with open(filename, 'r') as f:
        yamlObject = yaml.safe_load(f)

    batsmen_data = {}
    bowler_data = {}
    batsman_v_bowler = {}
    innings_data = {}

    for inning in yamlObject['innings']:
        for k in inning:
            team = inning[k]['team']
            if team not in batsmen_data:
                batsmen_data[team] = {}
                bowler_data[team] = {}
                batsman_v_bowler[team] = {}
                innings_data[team] = {}

            deliveries = inning[k]['deliveries']
            for i in range(len(deliveries)):
                key = list(deliveries[i].keys())[0]

                ballInfo = deliveries[i][key]

                batsman = ballInfo['batsman']
                non_striker = ballInfo['non_striker']
                bowler = ballInfo['bowler']

                if batsman not in innings_data[team]:
                    innings_data[team][batsman] = {k}
                if non_striker not in innings_data[team]:
                    innings_data[team][non_striker] = {k}

                innings_data[team][batsman].add(k)
                innings_data[team][non_striker].add(k)

                runs = ballInfo['runs']['batsman']

                forward_label = batsman + ',' + non_striker
                backward_label = non_striker + ',' + batsman

                batsman_v_bowler_label = batsman + ',' + bowler
                
                if forward_label not in batsmen_data[team]:
                    batsmen_data[team][backward_label] = 0
                    batsmen_data[team][forward_label] = 0
                
                if batsman_v_bowler_label not in batsman_v_bowler[team]:
                    batsman_v_bowler[team][batsman_v_bowler_label] = 0

                batsmen_data[team][forward_label] += runs
                batsman_v_bowler[team][batsman_v_bowler_label] += runs

                if 'wicket' in ballInfo:
                    player_out = ballInfo['wicket']['player_out']

                    forward_label = bowler + ',' + player_out
                    if forward_label not in bowler_data[team]:
                        bowler_data[team][forward_label] = 0    
                    bowler_data[team][forward_label] += 1
    
    for team in batsmen_data:
        with open(partnership_prefix + '_' + team.lower() + '.csv', 'w') as f:
            # line_to_write = 'scorer,partner,runs\n'
            # f.write(line_to_write)
            for k in batsmen_data[team]:
                line_to_write = k + ',' + str(batsmen_data[team][k]) + '\n'
                f.write(line_to_write)
    
    for team in bowler_data:
        with open(wickets_prefix + '_' + team.lower() + '.csv', 'w') as f:
            # line_to_write = 'bowler,batsman\n'
            # f.write(line_to_write)
            for k in bowler_data[team]:
                line_to_write = k + ',' + str(bowler_data[team][k]) + '\n'
                f.write(line_to_write)

    for team in batsman_v_bowler:
        with open(performance_prefix + '_' + team.lower() + '.csv', 'w') as f:
            for k in batsman_v_bowler[team]:
                line_to_write = k + ',' + str(batsman_v_bowler[team][k]) + '\n'
                f.write(line_to_write)

    for team in innings_data:
        with open(innings_prefix + '_' + team.lower() + '.csv', 'w') as f:
            for batsman in innings_data[team]:
                line_to_write = batsman + ',' + str(len(innings_data[team][batsman])) + '\n'
                f.write(line_to_write)
