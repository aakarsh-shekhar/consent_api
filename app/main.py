from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import uuid
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boosted_tech_consent_api.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Consent(db.Model):
    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    consent_url = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    version = db.Column(db.Integer, default=0, nullable=False)
    # Every time a modification is made to a target, the entire row is duplicated,
    #  the change is applied and this integer is incremented by 1. Starting at 0

    def __repr__(self):
        return '<Consent %s>' % self.name

# only run once on init
with app.app_context():
    db.create_all()

    # db.session.add(User('admin', 'admin@example.com'))
    # db.session.add(User('guest', 'guest@example.com'))
    # db.session.commit()

    consent = Consent.query.all()
    print(consent)
    print("***")

class ConsentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "consent_url", "created_at", "version")

consent_schema = ConsentSchema()
consents_schema = ConsentSchema(many=True)

class ConsentTargetsResource(Resource):
    def get(self):
        all_targets = Consent.query.all()
        return consents_schema.dump(all_targets)

    # def post(self):
    #     new_post = Post(
    #         title=request.json['title'],
    #         content=request.json['content']
    #     )
    #     db.session.add(new_post)
    #     db.session.commit()
    #     return post_schema.dump(new_post)


# class ConsentTargetResource(Resource):
#     def get(self, targetId):
#         post = Post.query.get_or_404(post_id)
#         return post_schema.dump(post)
#
#     def patch(self, targetId):
#         post = Post.query.get_or_404(post_id)
#
#         if 'title' in request.json:
#             post.title = request.json['title']
#         if 'content' in request.json:
#             post.content = request.json['content']
#
#         db.session.commit()
#         return post_schema.dump(post)
#
api.add_resource(ConsentTargetsResource, '/consent/target')
# api.add_resource(ConsentTargetResource, '/consent/target/<int:targetId>')

# sanity check
@app.route("/ping")
def test_route():
        return "<h1>Pong!</h1>"

# Start your app
if __name__ == '__main__':
    app.run(port=4242)
