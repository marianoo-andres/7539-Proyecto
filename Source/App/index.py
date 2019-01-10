from flask import Flask, request
import socket
import os
def getLocalIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

app = Flask(__name__)


@app.route('/', methods=["POST"])
def index():
    data = request.get_json(force=True)["data"]
    data = data.replace("\n", "").replace("\t","")
    print(data)
    file = open(os.path.join("Temp","data.txt"), "w")
    file.write(data)
    file.close()
    return 'OK!'

if __name__ == "__main__":
    print("LOCAL IP IS: {}".format(getLocalIp()))
    app.run(host='0.0.0.0', port='5000')
