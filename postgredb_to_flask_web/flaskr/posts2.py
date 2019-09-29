from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGREDB_FILEPATH = ''
app.config.update(
     SQLALCHEMY_DATABASE_URI=POSTGREDB_FILEPATH
     SQLALCHEMY_TRACK_MODIFICATIONS=False
     )
     
db = SQLAlchemy(app)

def index():
       return render_template(‘posts.html’)

if __name__ == '__main__':
          app.run(debug = True)
