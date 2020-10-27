# WCZ
APIs to access cricket match data \
Database used: SQLite


## Setup commands
git clone https://github.com/iamtanay7/WCZ.git \
cd WCZ \
python3 -m venv venv \
source venv/bin/activate \
pip install -r requirements.txt 


## start server
export FLASK_APP=main.py \
flask run

## API to get information about all matches, sorted by date
command:
curl http://localhost:5000/matches \
output: \
[{"victory_margin": "4 runs", 
"second_team_name": "England", 
"date_played": "2020-09-10", 
"first_team_name": "India", 
"winning_team_name": "England"}, \
{"victory_margin": "3 wickets", "second_team_name": "England", "date_played": "2020-05-17", "first_team_name": "India", "winning_team_name": "England"}, \
{"victory_margin": "4 runs", "second_team_name": "England", "date_played": "2020-05-17", "first_team_name": "India", "winning_team_name": "England"}] 

## API to get information about one match
command: curl http://localhost:5000/match/1 \
output: \
{"date_played":"Sun, 17 May 2020 00:00:00 GMT",\
"first_team_details":{"captain_name":"Virat Kohli","coach_name":"Ravi Shastri","matches_played":3,"team_name":"India"},\
"first_team_fours":6,"first_team_name":"India","first_team_score":78,"first_team_sixes":3,"first_team_wickets":7,\
"second_team_details":{"captain_name":"Eoin Morgan","coach_name":"Chris Silverwood","matches_played":3,"team_name":"England"},\
"second_team_fours":12,"second_team_name":"England","second_team_score":96,"second_team_sixes":5,"second_team_wickets":10,\
"victory_margin":"3 wickets",\
"winning_team_name":"England"}



## API to get information about all teams
command: \
curl http://localhost:5000/teams
[{"captain_name": "Virat Kohli", "team_name": "India", "coach_name": "Ravi Shastri"}, \
{"captain_name": "Eoin Morgan", "team_name": "England", "coach_name": "Chris Silverwood"}]

## API to add a new team
command: \
curl http://localhost:5000/teams -X POST -H "content-Type:application.json" -d '{"team_name":"India", "captain_name":"Virat Kohli", "coach_name":"Ravi Shastri"}'

## API to add a new match
command: \
curl http://localhost:5000/matches -X POST -H "content-Type:application.json" -d '{"first_team_name":"India",
"first_team_score": 100,
"first_team_fours": 6,
"first_team_sixes": 3,
"first_team_wickets": 7,
"second_team_name": "England",
"second_team_score": 96,
"second_team_fours": 12,
"second_team_sixes": 5,
"second_team_wickets": 10,
"winning_team_name": "England",
"man_of_the_match": "Virat Kohli",
"victory_margin": "4 runs"
 }'
