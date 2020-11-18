import os
from time import time
from math import ceil
from extract_and_dump import extract_and_dump

input_folder = './tests'
output_folder = './processed'

yaml_files = os.listdir(input_folder)

width = 100
stat_line = '[ ETA : XXX:XX:XX ] [' + '.' * width + ']'
proc_times = []
errored_files = []

print(stat_line, end='\r')

for index, yaml_file in enumerate(yaml_files, 1):

    proc_begin = time()

    # file names
    name, ext = os.path.splitext(yaml_file)
    file_path = input_folder + '/' + yaml_file
    partnership_prefix = output_folder + '/partnership_' + name
    wickets_prefix = output_folder + '/wickets_' + name
    performance_prefix = output_folder + '/performance_' + name
    innings_prefix = output_folder + '/innings_' + name

    # core process
    try:
        extract_and_dump(file_path, partnership_prefix, wickets_prefix, performance_prefix, innings_prefix)
    except Exception as e:
        error_details = yaml_file + ' - ' + str(e)
        errored_files.append(error_details)

    # estimate ETA
    proc_end = time()
    elapsed_time = proc_end - proc_begin
    proc_times.append(elapsed_time)

    eta = sum(proc_times) / index
    eta = ceil(eta * (len(yaml_files)-index))
    
    hours = str(eta // (60 * 60)).zfill(3)
    eta = eta % (60 * 60)
    mins = str(eta // 60).zfill(2)
    eta = eta % 60
    secs = str(eta).zfill(2)

    # format status line
    eta = ':'.join([hours, mins, secs])
    completed_width = (index * width) // len(yaml_files)
    stat_line = '[ ETA : {} ] '.format(eta) + '[' + completed_width * '*' + (width-completed_width) * '.' + ']'

    print(stat_line, end='\r')

with open('errors.txt', 'w') as f:
    for e in errored_files:
        f.write(e+'\n')

print()
