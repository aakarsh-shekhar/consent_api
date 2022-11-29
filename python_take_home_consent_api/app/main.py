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
    uid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    consent_url = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    version = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return '<Consent %s>' % self.name

with app.app_context():
    db.create_all()
    # -- sanity check --
    # consent = Consent.query.all()
    # print(consent)
    # print("***")

class ConsentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "consent_url", "created_at", "version")

consent_schema = ConsentSchema()
consents_schema = ConsentSchema(many=True)

class ConsentTargetsResource(Resource):
    def get(self):
        all_targets = Consent.query.all()
        return consents_schema.dump(all_targets)

    def post(self):
        new_consent = Consent(
            name=request.json['name'],
            consent_url=request.json['consent_url']
        )
        db.session.add(new_consent)
        db.session.commit()
        return consent_schema.dump(new_consent)


class ConsentTargetResource(Resource):
    def get(self, targetId):
        consents = Consent.query.filter_by(id=targetId).all()
        return consents_schema.dump(consents)

    def patch(self, targetId):
        consent = Consent.query.filter_by(id=targetId).order_by(Consent.version.desc()).first()

        new_consent = Consent(
            id=consent.id,
            name=consent.name,
            consent_url=request.json['consent_url'],
            version=consent.version+1
        )
        db.session.add(new_consent)
        db.session.commit()
        return consent_schema.dump(new_consent)

api.add_resource(ConsentTargetsResource, '/consent/target')
api.add_resource(ConsentTargetResource, '/consent/target/<targetId>')

# sanity check
@app.route("/ping")
def test_route():
        return "<h1>Pong!</h1>"

# Start your app
if __name__ == '__main__':
    app.run(port=4242)
