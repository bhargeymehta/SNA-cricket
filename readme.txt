Notes:
1. Based on work done by Dr. Satyam Mukherjee
    a. https://doi.org/10.1142/S0219525913500318
    b. https://doi.org/10.1016/j.physa.2013.09.027
2. Ball by ball data available on https://cricsheet.org/
3. Following folders to be created in same location
    a. tests
    b. teamwise
    c. processed
    d. pib_qib_stats
4. Flow of scripts
    a. process.py -> compile.py -> realise_pib_qib.py
5. Script name: extract_and_dump.py
    a. Contains logic to parse yaml file and output required data for one match file.
6. Script name: process.py
    a. Driver for the extract_and_dump.py script
    b. Will produce error logs and handles other non-core logic
    c. Input folder: tests
    d. Output folder: processed
7. Script name: compile.py
    a. Compiles data for all matches into single file for teams
    b. Also produces a general_stats log file for a summary of data
    c. Input folder: processed
    d. Output folder: teamwise
8. Script name: realise_pib_qib.py
    a. Calculates additional data required to realise the PIB and QIB networks
    b. Input folder: teamwise
    c. Output folder: pib_qib_stats
9. Folder name: tests
    a. Shoud contain the ball-by-ball data in yaml format as provided by cricsheet.org
    b. Some cases have not been handled in which case the file name and corresponding errors will be present in an errors.txt log file generated after script completes.
10. Folder name: processed
    a. Will contain the required data in a matchwise format.
    b. 4 files are generated for each match.
11. Folder name: teamwise
    a. Will contain the required data of all the matches across teams
12. Folder name: pib_qib_stats
    a. Will contain the required data to realise PIB and QIB networks
13. Important files used in the jupyter notebook
    a. Bowler and batsman career averages (present in folder- pib_qib_stats)
    b. Bowler-Batsman wise pairs of career history (present in folder- pib_qib_stats)
    c. Partnership files (present in folder- teamwise)
