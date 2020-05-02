from flask import Flask
from flask_toastr import Toastr
toastr = Toastr()

app = Flask(__name__)
app.secret_key = "secret key"
toastr.init_app(app)