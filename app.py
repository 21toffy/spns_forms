from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from datetime import datetime


app = Flask(__name__)

ENV= 'prod'
if ENV =='dev':
	app.debug =True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://spns_user:spns_password@localhost/spns_forms'
else:
	app.debug =False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uzochtymrvxwhs:bde5ae7cb313369fc2d36c9c0db9288304e0c62c185ffa2273e43d3cae26aa81@ec2-54-242-120-138.compute-1.amazonaws.com:5432/d2osrhl76cjra3'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False



db = SQLAlchemy(app)
cors = CORS(app)


class DownloadForm(db.Model):
	__tablename__='downloadform'
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	name = db.Column(db.String(200))
	email = db.Column(db.String(200))
	phone = db.Column(db.String(200))
	company = db.Column(db.String(200))
	service = db.Column(db.String(200))
	acknowledged = db.Column(db.Boolean, default=False, nullable=False)
		
@app.route('/get-downloads', methods=['GET'])
@cross_origin()
def get_downloads():
	downloads = DownloadForm.query.all()
	output = []
	for download in downloads:
		download_data = {}
		download_data ['name'] = download.name
		download_data ['email'] = download.email
		download_data ['phone'] = download.phone
		download_data ['company'] = download.company
		download_data ['service'] = download.service
		download_data ['date'] = download.date
		download_data ['acknowledged'] = download.acknowledged
		output.append(download_data)
	return jsonify({"downloads":output})


@app.route('/download-form', methods=['POST'])
@cross_origin()
def download_form():
	data = request.get_json()
	try:
		new_download = DownloadForm(name=data['name'], email=data['email'], phone=data['phone'], company=data['company'], service=data['service'])
		db.session.add(new_download)
		db.session.commit()
		return jsonify({"message": "New download recorded!"})
	except Exception as e:
		response_object = {
            'status': 'fail',
            'message': e
        }

		return jsonify(response_object), 400
    # except Exception as e:
    #     response_object = {
    #         'status': 'fail',
    #         'message': e
    #     }
    #     return response_object, 200



@app.route('/delete-downloads/<id>', methods=['DELETE'])
@cross_origin()
def delete_download(id):
	download = DownloadForm.query.get(id)
	db.session.delete()
	db.session.commit()
	return jsonify({"message": "Download entry deleted"})



# if __name__=="__main__":
# 	app.run()