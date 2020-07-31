#from watson_machine_learning_client import WatsonMachineLearningAPIClient
import math
from cloudant import Cloudant
from flask import Flask, render_template, request,Response,jsonify
from http import cookies
import atexit
import os
import json

#For IBM cloud watson start

# wml_credentials =  {
#   "apikey": "SUjb5zGHRaHe2A9XTD3q33eklKbi69HbKfyylv4_NMz1",
#   "iam_apikey_description": "Auto-generated for key cdb767c0-ed3f-4885-b73b-984b666f7cc5",
#   "iam_apikey_name": "Service credentials-1",
#   "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
#   "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/ada73095451441d9a0af1fd3af34974f::serviceid:ServiceId-8e8dc75b-ec6b-4a97-b643-112784e4e698",
#   "instance_id": "bda4dffe-cf02-4f03-8efd-b64959a951d9",
#   "password": "SUjb5zGHRaHe2A9XTD3q33eklKbi69HbKfyylv4_NMz1",
#   "username": "SUjb5zGHRaHe2A9XTD3q33eklKbi69HbKfyylv4_NMz1",
#   "url": "https://eu-gb.ml.cloud.ibm.com"
# }
# client = WatsonMachineLearningAPIClient( wml_credentials )

# #
# # 2.  Fill in one or both of these:
# #     - model_deployment_endpoint_url
# #     - function_deployment_endpoint_url
# #
# model_deployment_endpoint_url    = ""
# function_deployment_endpoint_url = ""

# def createPayload( canvas_data ):
#     dimension      = canvas_data["height"]
#     img            = Image.fromarray( np.asarray( canvas_data["data"] ).astype('uint8').reshape( dimension, dimension, 4 ), 'RGBA' )
#     sm_img         = img.resize( ( 28, 28 ), Image.LANCZOS )
#     alpha_arr      = np.array( sm_img.split()[-1] )
#     norm_alpha_arr = alpha_arr / 255
#     payload_arr    = norm_alpha_arr.reshape( 1, 784 )
#     payload_list   = payload_arr.tolist()
#     return { "values" : payload_list }

#End IBM cloud watson start



app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('login.html')

@app.route('/dashboard')
def dashboard():
    cokkie=request.cookies.get("user_infi")
    return app.send_static_file('dashboard.html')

@app.route('/devices')
def devices():
    cokkie=request.cookies.get("user_infi")
    return app.send_static_file('devices.html')

@app.route('/login')
def login():
    return app.send_static_file('login.html')

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)

#User log in post method 
@app.route('/api/userlogin', methods=['POST'])
def user_login():
    result=None
    if client:
        db = client.create_database('users', throw_on_exists=False)
        selector = {'username': {'$eq': request.json['username']},'password': {'$eq': request.json['password']}}
        docs = db.get_query_result(selector)
        for doc in docs:
            result=docs[0]
        return jsonify(result)
    else:
        print('No database')
        return jsonify(result)

# API for inserting total usage data to table
@app.route('/api/addtotalusage', methods=['POST'])
def add_total_usage():
    #user = request.json['name']
    postalcode=71141
    yearmonth= request.json['yearmonth']
    gallons= request.json['totalgallons']
    data = {'PostalCode':postalcode,'TotalGallons':gallons,'YearMonth':yearmonth}
    if client:
        db = client.create_database('mydb', throw_on_exists=False)
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)

#API for getting gallons data
@app.route('/api/gettotalusage', methods=['POST'])
def get_total_usage():
    result=[]
    if client:
        db = client.create_database('database1', throw_on_exists=False)
        #selector = {'PostalCode': {'$eq': request.json['postalcode']}}
        selector = {'_id': {'$gt': "0"}}
        docs = db.get_query_result(selector)
        for doc in docs:
            result.append(doc)
        return jsonify(result)
    else:
        print('No database')
        return jsonify(result)

#API for getting devices
@app.route('/api/getdevices', methods=['GET'])
def get_devices():
    result=[]
    if client:
        db = client.create_database('devices', throw_on_exists=False)
        #selector = {'PostalCode': {'$eq': request.json['postalcode']}}
        selector = {'_id': {'$gt': "0"}}
        docs = db.get_query_result(selector)
        for doc in docs:
            result.append(doc)
        return jsonify(result)
    else:
        print('No database')
        return jsonify(result)


# API for New device installation
@app.route('/api/newinstall', methods=['POST'])
def new_install():
    data = request.json
    if client:
        db = client.create_database('devices', throw_on_exists=False)
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)


@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
