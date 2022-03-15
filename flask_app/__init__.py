from flask import Flask, render_template, redirect, request, session
app = Flask(__name__)
app.secret_key = "shhhhhh"

DATABASE = 'mangalog_schema'

from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)