from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/thehive',methods=['POST', 'GET'])
def foo():
   data = json.loads(request.data)
   print(json.dumps(data, indent=4))
   return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
