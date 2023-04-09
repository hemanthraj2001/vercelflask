import openai
import requests


from bs4 import BeautifulSoup
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

#chat_gpt_cred

openai.api_key = 'SECRET_KEY'
query = "From the given text return only medicines names in it :"
#medicine_api
base_query_url = 'https://www.apollopharmacy.in/search-medicines/'
base_result_url = 'https://www.apollopharmacy.in'

class Prescription(Resource):


    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', required=True, location='args')
        args = parser.parse_args()
        user_text = args['text']
        #chatGPT_API
        text_op = " "
        text_op = text_op.join(user_text)
        input_text = query + text_op
        answer = openai.ChatCompletion.create(model = "gpt-3.5-turbo",messages=[{"role":"user","content": input_text}])
        reply_content = answer.choices[0].message.content # type: ignore
        return {'text': reply_content},200 # return data with 200 OK 

class Medicine(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q',required=True,location='args')
        args = parser.parse_args()
        query = args['q']
        query = query.replace(' ','%20')
        print(query)
        q_url = base_query_url + query
        r = requests.get(q_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        containers = soup.find_all("div",attrs={"class": "ProductCard_pdHeader__ETKkp"})
        prod = containers[0].a['href']
        prod_url = base_result_url + prod
        return {'medicine_url': prod_url},200

class Home(Resource):
    def post(self):
        return 'Hello!'
    def get(self):
        return 'Hi!'

api.add_resource(Prescription, '/user_text')  # add endpoints
api.add_resource(Medicine,'/medicine')
api.add_resource(Home,'/')



if __name__ == '__main__':
    app.run()  # run our Flask app