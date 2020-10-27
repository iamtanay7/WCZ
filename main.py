from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy # new
from flask_marshmallow import Marshmallow # new
from flask_restful import Api, Resource # new
import json, datetime
from json import JSONEncoder


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # new
db = SQLAlchemy(app) # new
ma = Marshmallow(app)
api = Api(app)

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	team_name = db.Column(db.String(50), unique = True)
	captain_name = db.Column(db.String(50))
	coach_name = db.Column(db.String(50))
	
	def __repr__(self):
        	return '<Team name %s>' % self.team_name	






class TeamSchema(ma.Schema):
	class Meta:
		model = Team
		fields = ("team_name", "captain_name", "coach_name")
		

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

class TeamListResource(Resource):
	def get(self):
		teams = Team.query.all()
		return teams_schema.dump(teams)

    
	def post(self):
		temp = request.get_data()
		temp=json.loads(temp)
		new_team = Team(
			team_name=temp['team_name'],
			captain_name=temp['captain_name'],
			coach_name=temp['coach_name']
			)
		db.session.add(new_team)
		db.session.commit()
		print(temp)
		return team_schema.dump(new_team)

api.add_resource(TeamListResource, '/teams')

class Match(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_played = db.Column(db.Date)
	first_team_name = db.Column(db.String(50))
	second_team_name = db.Column(db.String(50))
	first_team_sixes = db.Column(db.Integer)
	second_team_sixes = db.Column(db.Integer)
	first_team_fours = db.Column(db.Integer)
	second_team_fours = db.Column(db.Integer)
	first_team_score = db.Column(db.Integer)
	second_team_score = db.Column(db.Integer)
	first_team_wickets = db.Column(db.Integer)
	second_team_wickets = db.Column(db.Integer)
	winning_team_name = db.Column(db.String(50))
	man_of_the_match = db.Column(db.String(50))
	victory_margin = db.Column(db.String(50))



class MatchSchema(ma.Schema):
	class Meta:
		model = Match
		fields = ("date_played","first_team_name","first_team_score","first_team_fours",
			"first_team_sixes","first_team_wickets", "second_team_name", "second_team_score",
			"second_team_fours", "second_team_sixes", "second_team_sixes", "winning_team_id", 
			"man_of_the_match" )

class MatchListSchema(ma.Schema):
	class Meta:
		model = Match
		fields = ("date_played", "first_team_name", "second_team_name",
			"winning_team_name", "victory_margin")



match_schema = MatchSchema()
matches_schema = MatchListSchema(many = True)

class MatchListResource(Resource):
	def get(self):
		matches = Match.query.order_by(Match.date_played.desc())
		return matches_schema.dump(matches)


	def post(self):
		temp = request.get_data()
		temp = json.loads(temp)
		new_match = Match(
				date_played = datetime.datetime(2020,9,10),
				first_team_name = temp['first_team_name'],
				first_team_score = temp['first_team_score'],
				first_team_wickets = temp['first_team_wickets'],
				winning_team_name = temp['winning_team_name'],
				first_team_sixes = temp['first_team_sixes'],
				first_team_fours = temp['first_team_fours'],
				second_team_name = temp['second_team_name'],
				second_team_score = temp['second_team_score'],
				second_team_fours = temp['second_team_fours'],
				second_team_sixes = temp['second_team_sixes'],
				second_team_wickets = temp['second_team_wickets'],
				man_of_the_match = temp['man_of_the_match'],
				victory_margin = temp['victory_margin'],

			)
		db.session.add(new_match)
		db.session.commit()
		print(new_match)
		return match_schema.dump(new_match)


api.add_resource(MatchListResource,'/matches')

class MatchEncoder(JSONEncoder):
	def default(self,o):
		return o.__dict__



class MatchResource(Resource):
	def get(self,id):
		match = Match.query.get_or_404(id)
		team1 = Team.query.filter_by(team_name=match.first_team_name).first()
		team2 = Team.query.filter_by(team_name=match.second_team_name).first()
		team1_matches = Match.query.filter_by(first_team_name=team1.team_name).count()+Match.query.filter_by(second_team_name=team1.team_name).count()

		team2_matches = Match.query.filter_by(first_team_name=team2.team_name).count()+Match.query.filter_by(second_team_name=team2.team_name).count()
		print(team1_matches,team2_matches)
		return jsonify({
			"date_played":match.date_played,

			"first_team_name":match.first_team_name,
			"second_team_name":match.second_team_name,
			"winning_team_name":match.winning_team_name,
			"victory_margin":match.victory_margin,
			"first_team_score":match.first_team_score,
			"first_team_fours":match.first_team_fours,
			"first_team_sixes":match.first_team_sixes,
			"first_team_wickets":match.first_team_wickets,			
			"second_team_score":match.second_team_score,
			"second_team_fours":match.second_team_fours,
			"second_team_sixes":match.second_team_sixes,
			"second_team_wickets":match.second_team_wickets,
			"first_team_details":{
			"team_name":team1.team_name,
			"captain_name":team1.captain_name,
			"coach_name":team1.coach_name,
			"matches_played":team1_matches,

			},
			"second_team_details":{
			"team_name":team2.team_name,
			"captain_name":team2.captain_name,
			"coach_name":team2.coach_name,
			"matches_played":team2_matches,
			
			}

			})


		

api.add_resource(MatchResource,'/match/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)

