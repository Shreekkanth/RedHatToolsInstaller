from functools import wraps
from flask import Flask, request, Response
from flask_restful import abort, Resource, Api, fields, marshal_with, reqparse
import status
from models import ItemModel
from json import dumps
import os

app = Flask(__name__)
api = Api(app)


class CmdbManager():
    last_id = 0

    def __init__(self):
            
        self.items = {

           1: {
                "id": 1,
                "fqdn": "server01.mydomain.com",
                "ip_address": "192.168.30.11",
                "mac_address": "00:01:B7:23:F1:01",
                "owned_by": "Mario Speedwagon",
                "serial_number": "vF435F"
            },
           2: {
                "id": 2,
                "fqdn": "server02.mydomain.com",
                "ip_address": "192.168.30.12",
                "mac_address": "00:01:B7:23:F1:02",
                "owned_by": "Petey Cruiser",
                "serial_number": "7rGGTs"
            },
           3: {
                "id": 3,
                "fqdn": "server03.mydomain.com",
                "ip_address": "192.168.30.13",
                "mac_address": "00:01:B7:23:F1:03",
                "owned_by": "Anna Sthesia",
                "serial_number": "8nCbZV"
            },
           4: {
                "id": 4,
                "fqdn": "server04.mydomain.com",
                "ip_address": "192.168.30.14",
                "mac_address": "00:01:B7:23:F1:04",
                "owned_by": "Paul Molive",
                "serial_number": "AW8htC"
            },
           5: {
                "id": 5,
                "fqdn": "server02.mydomain.com",
                "ip_address": "192.168.30.15",
                "mac_address": "00:01:B7:23:F1:05",
                "owned_by": "Anna Mull",
                "serial_number": "Adj6Fp"
            },
            6: {
                "id": 6,
                "fqdn": "server06.mydomain.com",
                "ip_address": "192.168.30.16",
                "mac_address": "00:01:B7:23:F1:06",
                "owned_by": "Gail Forcewind",
                "serial_number": "CAzya7"
            },
            7: {
                "id": 7,
                "fqdn": "server07.mydomain.com",
                "ip_address": "192.168.30.17",
                "mac_address": "00:01:B7:23:F1:07",
                "owned_by": "Paige Turner",
                "serial_number": "CbjeaR"
            },
            8: {
                "id": 8,
                "fqdn": "server08.mydomain.com",
                "ip_address": "192.168.30.18",
                "mac_address": "00:01:B7:23:F1:08",
                "owned_by": "Bob Frapples",
                "serial_number": "CwteZJ"
            },
            9: {
                "id": 9,
                "fqdn": "server09.mydomain.com",
                "ip_address": "192.168.30.19",
                "mac_address": "00:01:B7:23:F1:09",
                "owned_by": "Walter Melon",
                "serial_number": "DT4TqG"
            },
            10: {
                "id": 10,
                "fqdn": "server10.mydomain.com",
                "ip_address": "192.168.30.20",
                "mac_address": "00:01:B7:23:F1:10",
                "owned_by": "Nick R. Bocker",
                "serial_number": "EteKQM"
            },
            11: {
                "id": 11,
                "fqdn": "server11.mydomain.com",
                "ip_address": "192.168.30.21",
                "mac_address": "00:01:B7:23:F1:11",
                "owned_by": "Barb Ackue",
                "serial_number": "FeruuV"
            },
            12: {
                "id": 12,
                "fqdn": "server12.mydomain.com",
                "ip_address": "192.168.30.22",
                "mac_address": "00:01:B7:23:F1:12",
                "owned_by": "Buck Kinnear",
                "serial_number": "KFRNU4"
            },
            13: {
                "id": 13,
                "fqdn": "server13.mydomain.com",
                "ip_address": "192.168.30.23",
                "mac_address": "00:01:B7:23:F1:13",
                "owned_by": "Greta Life",
                "serial_number": "M9vzVd"
            },
            14: {
                "id": 14,
                "fqdn": "server14.mydomain.com",
                "ip_address": "192.168.30.24",
                "mac_address": "00:01:B7:23:F1:14",
                "owned_by": "Ira Membrit",
                "serial_number": "MjV5K4"
            },
            15: {
                "id": 15,
                "fqdn": "server13.mydomain.com",
                "ip_address": "192.168.30.25",
                "mac_address": "00:01:B7:23:F1:15",
                "owned_by": "Shonda Leer",
                "serial_number": "NZUAXu"
            },
            16: {
                "id": 16,
                "fqdn": "server13.mydomain.com",
                "ip_address": "192.168.30.26",
                "mac_address": "00:01:B7:23:F1:16",
                "owned_by": "Brock Lee",
                "serial_number": "SZAabU"
            },
            17: {
                "id": 17,
                "fqdn": "server17.mydomain.com",
                "ip_address": "192.168.30.27",
                "mac_address": "00:01:B7:23:F1:17",
                "owned_by": "Maya Didas",
                "serial_number": "Wyk55y"
            },
            18: {
                "id": 18,
                "fqdn": "server18.mydomain.com",
                "ip_address": "192.168.30.28",
                "mac_address": "00:01:B7:23:F1:18",
                "owned_by": "Rick O'Shea",
                "serial_number": "YozE2Z"
            },
            19: {
                "id": 19,
                "fqdn": "server13.mydomain.com",
                "ip_address": "192.168.30.29",
                "mac_address": "00:01:B7:23:F1:19",
                "owned_by": "Pete Sariya",
                "serial_number": "Ywi5k4"
            },
            20: {
                "id": 20,
                "fqdn": "server30.mydomain.com",
                "ip_address": "192.168.30.30",
                "mac_address": "00:01:B7:23:F1:20",
                "owned_by": "Monty Carlo",
                "serial_number": "ZZ8hsu"
            },
        }

        self.__class__.last_id = len(self.items)

    def insert_item(self, item):
        """This method receives a recently created MessageModel instance in the message argument"""
        self.__class__.last_id += 1
        item.id = self.__class__.last_id
        self.items[self.__class__.last_id] = item

    def get_item(self, id):
        """This method receives the id of the message that has to be retrieved from the self.messages dictionary."""
        return self.items[id]


    def delete_item(self, id):
        """This method receives the id of the message that has to be removed from the self.messages dictionary"""
        del self.items[id]


cmdb_fields = {
    'id': fields.Integer,
	'fqdn': fields.String,
	'ip_address': fields.String,
	'mac_address': fields.String,
	'owned_by': fields.String,
	'serial_number': fields.String
}


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    username_valid = os.getenv("VALID_USERNAME",'admin')
    password_valid = os.getenv("VALID_PASSWORD",'secret')

    return username == username_valid and password == password_valid

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


cmdb_manager = CmdbManager()

class CmdbItem(Resource):
    	def abort_if_item_doesnt_exist(self, id):
		if id not in cmdb_manager.items:
			abort(status.HTTP_404_NOT_FOUND,
				message = "Message {0} doesnot exists".format(id)
			)


	@marshal_with(cmdb_fields)
	def get(self, id):
		self.abort_if_item_doesnt_exist(id)
		return cmdb_manager.get_item(id)



	def delete(self, id):
		self.abort_if_item_doesnt_exist(id)
		cmdb_manager.delete_item(id)
		return '', status.HTTP_204_NO_CONTENT

class CmdbList(Resource):

    @marshal_with(cmdb_fields)
    def get(self):
        return [v for v in cmdb_manager.items.values()]

    @requires_auth
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fqdn', type=str, required=True, help='FQDN cannot be blank!')
        parser.add_argument('ip_address', type=str, required=True, help='IP Address cannot be blank!')
        parser.add_argument('mac_address', type=str, required=True, help='MAC Address cannot be blank!')
        parser.add_argument('owned_by', type=str, required=True, help='Owned By cannot be blank!')
        parser.add_argument('serial_number', type=str, required=True, help='Serial Number Address cannot be blank!')

        args = parser.parse_args()
        item = ItemModel(
            fqdn=args['fqdn'],
            ip_address=args['ip_address'],
            mac_address=args['mac_address'],
            owned_by=args['owned_by'],
            serial_number=args['serial_number']
            )
        cmdb_manager.insert_item(item) 
        #return message, status.HTTP_201_CREATED

        return Response(status=201)

class Health(Resource):
    
    def get(self):
        return Response(response="ok", content_type="text/plain",status=200)

api.add_resource(CmdbList, "/api/items")
api.add_resource(CmdbItem, "/api/items/<int:id>")
api.add_resource(Health, "/health") 

if __name__ == '__main__':
     app.run(host= '0.0.0.0')