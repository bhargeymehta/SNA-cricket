import os

input_folder = './teamwise'
output_folder = './pib_qib_stats'

team_files = sorted(os.listdir(input_folder))

batsman_role = {}
bowler_role = {}

for index, team_file in enumerate(team_files, 1):
    name, ext = os.path.splitext(team_file)

    dtype, team = name.split('_')
    if dtype == 'partnership':
        continue

    file_path = input_folder + '/' + team_file
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]
        
        if dtype == 'performance':
            for line in lines:
                batsman, bowler, runs = line.split(',')
                runs = int(runs)

                if batsman not in batsman_role:
                    batsman_role[batsman] = {
                        'total_innings': 0,
                        'total_runs': 0,
                        'total_dismisses': 0,
                        'against': {},
                        'dismissed_by': {}
                        }
                if bowler not in bowler_role:
                    bowler_role[bowler] = {
                        'total_dismisses': 0,
                        'total_runs': 0,
                        'wicket_of': {},
                        'runs_of': {}
                    }

                if bowler not in batsman_role[batsman]['against']:
                    batsman_role[batsman]['against'][bowler] = 0
                    batsman_role[batsman]['dismissed_by'][bowler] = 0

                if batsman not in bowler_role[bowler]['wicket_of']:
                    bowler_role[bowler]['wicket_of'][batsman] = 0
                    bowler_role[bowler]['runs_of'][batsman] = 0
                
                batsman_role[batsman]['against'][bowler] += runs
                batsman_role[batsman]['total_runs'] += runs

                bowler_role[bowler]['total_runs'] += runs
                bowler_role[bowler]['runs_of'][batsman] += runs
        elif dtype == 'wickets':
            for line in lines:
                bowler, batsman, times_dismissed = line.split(',')
                times_dismissed = int(times_dismissed)

                if batsman not in batsman_role:
                    batsman_role[batsman] = {
                        'total_innings': 0,
                        'total_runs': 0,
                        'total_dismisses': 0,
                        'against': {},
                        'dismissed_by': {}
                        }
                if bowler not in bowler_role:
                    bowler_role[bowler] = {
                        'total_dismisses': 0,
                        'total_runs': 0,
                        'wicket_of': {},
                        'runs_of': {}
                    }

                if bowler not in batsman_role[batsman]['against']:
                    batsman_role[batsman]['against'][bowler] = 0
                    batsman_role[batsman]['dismissed_by'][bowler] = 0

                if batsman not in bowler_role[bowler]['wicket_of']:
                    bowler_role[bowler]['wicket_of'][batsman] = 0
                    bowler_role[bowler]['runs_of'][batsman] = 0
                
                batsman_role[batsman]['total_dismisses'] += times_dismissed
                batsman_role[batsman]['dismissed_by'][bowler] += times_dismissed

                bowler_role[bowler]['total_dismisses'] += times_dismissed
                bowler_role[bowler]['wicket_of'][batsman] += times_dismissed
        elif dtype == 'innings':
            for line in lines:
                batsman, times_played = line.split(',')
                times_played = int(times_played)

                if batsman not in batsman_role:
                    batsman_role[batsman] = {
                        'total_innings': 0,
                        'total_runs': 0,
                        'total_dismisses': 0,
                        'against': {},
                        'dismissed_by': {}
                        }
                batsman_role[batsman]['total_innings'] += times_played
                

batsmen_averages_file_path = output_folder + '/' + 'batsmen_averages.csv'
bowlers_averages_file_path = output_folder + '/' + 'bowlers_averages.csv'

with open(batsmen_averages_file_path, 'w') as f:
    f.write('batsman,total_runs,total_innings\n')
    
    for batsman in batsman_role:
        runs = str(batsman_role[batsman]['total_runs'])
        innings = str(batsman_role[batsman]['total_innings'])
        
        line_to_write = batsman + ',' + runs + ',' + innings + '\n'
        f.write(line_to_write)

with open(bowlers_averages_file_path, 'w') as f:
    f.write('bowler,total_runs,total_dismisses\n')
    
    for bowler in bowler_role:
        runs = str(bowler_role[bowler]['total_runs'])
        dismisses = str(bowler_role[bowler]['total_dismisses'])
        
        line_to_write = bowler + ',' + runs + ',' + dismisses + '\n'
        f.write(line_to_write)

batsmen_against_bowlers_averages_file_path = output_folder + '/' + 'batsmen_against_bowlers_averages.csv'
bowlers_against_batsmen_averages_file_path = output_folder + '/' + 'bowlers_against_batsmen_averages.csv'

with open(batsmen_against_bowlers_averages_file_path, 'w') as f:
    f.write('batsman,bowler,runs,times_dismissed\n')
    
    for batsman in batsman_role:
        for bowler in batsman_role[batsman]['against']:
            runs = str(batsman_role[batsman]['against'][bowler])
            dismisses = str(batsman_role[batsman]['dismissed_by'][bowler])
        
            line_to_write = batsman + ',' + bowler + ',' + runs + ',' + dismisses + '\n'
            f.write(line_to_write)

with open(bowlers_against_batsmen_averages_file_path, 'w') as f:
    f.write('bowler,batsman,runs,times_dismissed\n')
    
    for bowler in bowler_role:
        for batsman in bowler_role[bowler]['wicket_of']:
            runs = str(bowler_role[bowler]['runs_of'][batsman])
            dismissed = str(bowler_role[bowler]['wicket_of'][batsman])
        
            line_to_write = bowler + ',' + batsman + ',' + runs + ',' + dismisses + '\n'
            f.write(line_to_write)
