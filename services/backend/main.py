
from flask import Flask,jsonify
from flask_restx import Api, Resource,fields,reqparse # type: ignore
from src.utils.logger import logging
from dotenv import load_dotenv


from src.utils.exception import CustomException
import sys
import os
from src.dataflow.rag_model import generateResponse
from flask_cors import CORS # type: ignore
load_dotenv(override=True)


app =Flask(__name__)

# Initialize Flask-RESTX API with Swagger support
api =Api(app, version="1.0" , title="NuBot Backend", description="Backend for NuBot")

CORS(app)
# create a namespace 
ns=api.namespace("NuBot",descrption="namespace for Backend")
parser = reqparse.RequestParser()
# Define a request model for Swagger UI
query_model = api.model('QueryModel', {
    'query': fields.String(required=True, description="User's input query")
})
@ns.route("/")
class Main(Resource):
    @api.expect(query_model)
    @api.response(200, "Success")
    @api.response(404, "Not Found")
    @api.response(500, "Internal Server Error")
    def post(self):
        """Return a simple message"""
        try:
            parser.add_argument('query', type=str, required=True, location='json', help="Query is required")
            args = parser.parse_args()
            if not args['query']:
                return {"error": "Query field is required"}, 400
            logging.info("Get api called")
            query=args['query']
            logging.info("response function called")
            response=generateResponse(query)
            logging.info("Response generated successfully")
            return response
        except Exception as e:
            logging.error("Custom exception occurred: %s", str(e))
            return jsonify({"error": "An internal server error occurred", "details": str(e)})
           

if __name__=="__main__":
    PORT=os.getenv('PORT', 8080)

    app.run(host='0.0.0.0',port=PORT,debug=True)