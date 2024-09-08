from flask import Flask, render_template
from WORKOUT_PROJECT import app



@app.route('/')
def home():
    SayHi = "운동기록 일지 서비스"
    return render_template('index.html', A = SayHi)
