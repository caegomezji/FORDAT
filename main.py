
from flask import Flask


app = Flask(config.app_name )

app.run(host="localhost", port="8080")
