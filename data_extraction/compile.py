import os

input_folder = './processed'
output_folder = './teamwise'

match_files = sorted(os.listdir(input_folder))

batsmen_data = {}
bowlers_data = {}
innings_data = {}
against_data = {}

batsmen = {}

team_times = {}

width = 100

for index, match_file in enumerate(match_files, 1):
    name, ext = os.path.splitext(match_file)

    dtype, code, team = name.split('_')

    if team not in batsmen_data:
        bowlers_data[team] = {}
        batsmen_data[team] = {}
        innings_data[team] = {}
        against_data[team] = {}

        batsmen[team] = set()
        team_times[team] = 0

    team_times[team] += 1

    file_path = input_folder + '/' + match_file
    
    if dtype == 'partnership':
        with open(file_path, 'r') as f:
            for line in f.readlines():
                scorer, partner, runs = line.strip().split(',')
                runs = int(runs)

                if scorer not in batsmen[team]:
                    batsmen[team].add(scorer)
                
                if partner not in batsmen[team]:
                    batsmen[team].add(partner)

                forward_label = scorer + ',' + partner
                backward_label = partner + ',' + scorer

                if forward_label not in batsmen_data[team]:
                    batsmen_data[team][forward_label] = 0
                    batsmen_data[team][backward_label] = 0

                batsmen_data[team][forward_label] += runs
    elif dtype == 'performance':
        with open(file_path, 'r') as f:
            for line in f.readlines():
                batsman, bowler, runs = line.strip().split(',')
                runs = int(runs)

                label = batsman + ',' + bowler

                if label not in against_data[team]:
                    against_data[team][label] = 0
                
                against_data[team][label] += runs
    elif dtype == 'innings':
        with open(file_path, 'r') as f:
            for line in f.readlines():
                batsman, times_played = line.strip().split(',')
                times_played = int(times_played)

                if batsman not in innings_data[team]:
                    innings_data[team][batsman] = 0
                innings_data[team][batsman] += times_played
    else:
        with open(file_path, 'r') as f:
            for line in f.readlines():
                bowler, batsman, times = line.strip().split(',')
                times = int(times)
                
                label = bowler + ',' + batsman
                
                if label not in bowlers_data[team]:
                    bowlers_data[team][label] = 0
                bowlers_data[team][label] += times

    completed_width = (index * width) // len(match_files)
    completed_percent = str(int(index * 100 / len(match_files))).zfill(3)
    stat_line = '[ Completed: {}% ] '.format(completed_percent) + '[' + completed_width * '*' + (width-completed_width) * '.' + ']'

    print(stat_line, end='\r')
print()

for team in bowlers_data:
    partnership_file_path = output_folder + '/partnership_' + team + '.csv'

    with open(partnership_file_path, 'w') as f:
        f.write('striker,non_striker,runs\n')
        for pair in batsmen_data[team]:
            runs = batsmen_data[team][pair]
            line_to_write = pair + ',' + str(runs) + '\n'
            f.write(line_to_write)

    wickets_file_path = output_folder + '/wickets_' + team + '.csv'
    with open(wickets_file_path, 'w') as f:
        f.write('bowler,batsman,times\n')
        for pair in bowlers_data[team]:
            times = bowlers_data[team][pair]
            line_to_write = pair + ',' + str(times) + '\n'
            f.write(line_to_write)

    performance_file_path = output_folder + '/performance_' + team + '.csv'
    with open(performance_file_path, 'w') as f:
        f.write('batsman,bowler,runs\n')
        for pair in against_data[team]:
            runs = against_data[team][pair]
            line_to_write = pair + ',' + str(runs) + '\n'
            f.write(line_to_write)

    innings_file_path = output_folder + '/innings_' + team + '.csv'
    with open(innings_file_path, 'w') as f:
        f.write('batsman,innings\n')
        for batsman in innings_data[team]:
            innings = innings_data[team][batsman]
            line_to_write = batsman + ',' + str(innings) + '\n'
            f.write(line_to_write)

general_stats = 'general_stats.txt'

with open(general_stats, 'w') as f:
    for team in batsmen_data:
        f.write('*' * 40 + ' ' + team + ' ' + '*' * 40 + '\n')
        if team_times[team] % 4 != 0:
            print('You are doomed!')

        f.write('Played in {} matches as per data.\n'.format(team_times[team] // 4))
        f.write('Batsmen : {}\n'.format(len(batsmen[team])))
        f.write('BPN Edges : {}\n'.format(len(batsmen_data[team])))
        
        f.write('\n\n')
