from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy # new
from flask_marshmallow import Marshmallow # new
from flask_restful import Api, Resource # new
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # new
db = SQLAlchemy(app) # new
ma = Marshmallow(app)
api = Api(app)

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	team_name = db.Column(db.String(50))
	captain_name = db.Column(db.String(50))
	coach_name = db.Column(db.String(50))
	
	def __repr__(self):
        	return '<Team name %s>' % self.team_name	

class TeamSchema(ma.Schema):
	class Meta:
		fields = ("id","team_name", "captain_name", "coach_name")
		model = Team

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





class TeamResource(Resource):
	def get(self, post_id):
		team = Team.query.get_or_404(post_id)
		return team_schema.dump(team)

api.add_resource(TeamListResource, '/teams')


	


if __name__ == '__main__':
    app.run(debug=True)
