from flask import Blueprint
import yfinance as yf
import pandas as pd
import mplfinance as mpf
from io import BytesIO
import base64

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "<h1>Hey there!</h1>"