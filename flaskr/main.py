
from turtle import color, position
from matplotlib.figure import Figure

from mysqlx import Column
from flaskr import app
from flask import render_template, redirect, url_for
from flask import request
import sqlite3
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

#------------------------------------
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import send_file
import io
import base64
import seaborn as sns

from flask import Flask, render_template, make_response
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import numpy as np



DATABASE = "baseball.db"

Columns = ["family_name","first_name","age","career","hometown","hand",\
        "bbox","position","uniform_number","team",\
        "ballSpeed","stamina","control",\
        "slider","cut","curve","fork","changeUp",\
        "era",\
        "meatAbility","powerAbility","trajectory",\
        "speedAbility","shoulderAbility","throwAbility","catchAbility",\
        "butting_average","hr","rbi","sb"
        ]

evals = {"meatAbility":"","powerAbility":"","speedAbility":"",\
        "shoulderAbility":"","throwAbility":"",\
        "catchAbility":""}
def get_eval(val):
    print("val:",val)
    val = int(val)
    eval = ""
    if val < 30: 
        eval = "G"
    elif val < 40:
        eval = "F"
    elif val < 50:
        eval = "E"
    elif val < 60:
        eval = "D"
    elif val < 70:
        eval = "C"
    elif val < 80:
        eval = "B"
    elif val < 90:
        eval = "A"
    elif val < 100:
        eval = "S"
    else: eval = "無効な値"

    return eval

def get_main_image():

    con = sqlite3.connect(DATABASE)

    df = pd.read_sql_query("SELECT * FROM player\
                     WHERE position='pitcher' ", con)
    con.close()

    df = df.loc[:,["ballSpeed","team"]]

    df_team = df.groupby("team").mean()
    x = df_team.index.to_list()
    y = df_team.loc[:,"ballSpeed"].to_list()
    plt.bar(x,y,color="blue")

    #値ラベルの追加
    for i in range(0, len(x)):
        plt.text(i,y[i]+2.0,y[i], ha="center")

    plt.xlabel("team")
    plt.ylabel("AVG(ballSpeed)")

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img

    

@app.route("/")
def index():
    return render_template(
        "index.html",
    )

@app.route('/form')
def form():
    return render_template(
        'form.html'
    )
@app.route('/avg_ranking')
def avg_ranking():
    return render_template(
        'avg_ranking.html'
    )

@app.route('/main.png')
def main_plot():
    img = get_main_image()
    return send_file(img,mimetype="image/png", cache_timeout=0)

@app.route('/avg_ranking',methods=["GET","POST"])
def ranking():
    return render_template(
        'form.html'
    )


@app.route('/library')
def library():
    
    # con = sqlite3.connect(DATABASE)

    # df = pd.read_sql_query("SELECT * FROM player", con)
    # con.close()

    

    # df = df.loc[:,["player_id","family_name","first_name",\
    #                 "age","position","team",\
    #                 "meatAbility","powerAbility","trajectory",\
    #                 "speedAbility","shoulderAbility",\
    #                 "throwAbility","catchAbility"]]


    con = sqlite3.connect(DATABASE)
    db_players = con.execute('SELECT * FROM player').fetchall()
    con.close()

    players = []
    for row in db_players:
        objs = [row[9],row[10],row[12],row[13],row[14],row[15],\
                row[16],row[19],row[20]]
        
        eval = [get_eval(i) for i in objs]

        players.append({"full_name":row[1]+" "+row[2],\
                        "age":row[3],"position":row[8],"team":row[18],\
                        "stamina": eval[6]+"("+str(row[16])+")",\
                        "control": eval[7] + "("+str(row[19])+")",\
                        "ballSpeed":row[17],\
                        "meat":eval[0]+"("+str(row[9])+")",\
                        "power":eval[1]+"("+str(row[10])+")",\
                        "trajectory":row[11],\
                        "speed":eval[2]+"("+str(row[12])+")",\
                        "shoulder":eval[3]+"("+str(row[13])+")",\
                        "throw":eval[4]+"("+str(row[14])+")",\
                        "catch":eval[5]+"("+str(row[15])+")"
                        })
    # players = df.to_html(classes = "table")
    return render_template(
        'library.html',
        players = players
    )


@app.route('/register', methods=["POST"])
def register():


    Values = [ 
        request.form["family_name"],request.form["first_name"],request.form["age"],\
        request.form["career"],request.form["hometown"], request.form["hand"],
        request.form["bbox"],request.form["position"],\
        request.form["uniform_number"],request.form["team"],\
        request.form["ballSpeed"],request.form["stamina"],request.form["control"],\
        request.form["slider"],request.form["cut"],request.form["curve"],\
        request.form["fork"],request.form["changeUp"],\
        request.form["era"],\
        request.form["meatAbility"],\
        request.form["powerAbility"],request.form["trajectory"],\
        request.form["speedAbility"],request.form["shoulderAbility"],\
        request.form["throwAbility"],request.form["catchAbility"],\
        request.form["butting_average"],request.form["hr"],\
        request.form["rbi"],request.form["sb"]\
        ]
    con= sqlite3.connect(DATABASE)
    df = pd.DataFrame([Values],columns = Columns)

    print("チーム名:",df["team"])

    df.to_sql("player",con, if_exists="append",index=False)

    con.commit()#コミット。ここでdbへ反映される。
    con.close()#DB切断。

    return redirect(url_for('index'))

    family_name = request.form["family_name"]

    