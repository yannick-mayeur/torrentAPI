from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug, os
import subprocess as sp

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['torrent'])

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Torrent(Resource):
    def get(self):
        p = sp.run(["transmission-remote", "-n", "transmission:transmission", "-l"], stdout=sp.PIPE)
	#TODO Interprétation du résultat
        return p.stdout.decode('utf-8')

    def post(self):
        data = parser.parse_args()
        if data['file'] == "":
            return {
                    'data':'',
                    'message':'No file found',
                    'status':'error'
                    }
        torrent = data['file']
        if torrent and allowed_file(torrent.filename):
            filename = torrent.filename
            torrent.save(os.path.join(UPLOAD_FOLDER,filename))
            return {
                    'data':'',
                    'message':'torrent uploaded',
                    'status':'success'
                    }
        return {
                'data':'',
                'message':'Something when wrong',
                'status':'error'
                }


api.add_resource(HelloWorld, '/')
api.add_resource(Torrent,'/torrents')

if __name__ == '__main__':
    app.run('0.0.0.0')
