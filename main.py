from flask import Flask, render_template, request,jsonify
import sqlite3
import continuousRecordingHopefully
# f=open("englishPhonemes.txt","r")
# lines=f.readlines()
# f.close()
# phonemes=["i","ɑ","u","ɔ","ɜ"]
global background_colour
background_colour="rgb(255,255,255)"
global RecordingDevice
global SoundLevel
SoundLevel=0
global Rvalue
Rvalue='R'
global Data
Data=""
global Svalue
Svalue="S"

app=Flask("app")

@app.route("/")
def Intro():
    return render_template("Introduction.html",background_color=background_colour)

@app.route("/Home")
def Home():
    return render_template("Table.html",background_color=background_colour)
 
@app.route("/Settings")
def Settings():
    return render_template("Settings.html",background_color=background_colour,value=Rvalue,svalue=Svalue)

@app.route("/Calibrate")
def Calibrate():
    return render_template("Calibrate.html",background_color=background_colour)

@app.route("/Document")
def Document():
    return render_template("Document.html",background_color=background_colour,output=Data)

@app.route('/pythonRecord', methods=['GET'])
def pythonRecord():
    global SoundLevel
    global RecordingDevice
    RecordingDevice=continuousRecordingHopefully.Recorder() #initiates a new instance of the recorder object
    RecordingDevice.changeThreshold(int(SoundLevel))
    data=RecordingDevice.listening()
    print("data=",data)
    del RecordingDevice
    return jsonify(data)

@app.route('/pythonStop', methods=['GET'])
def pythonStop():
    global RecordingDevice
    try:
        data=RecordingDevice.stop() #calls the stop function in the recorder
        del RecordingDevice
        return jsonify(data)
    except:
        return jsonify("")

@app.route('/submitColour',methods = ['POST'])
def submitColour():
    #takes the colour chosen by the user and stores it.
    global background_colour
    background_colour=request.get_json()
    return "Successful"

@app.route('/submitSound',methods = ['POST'])
def submitSound():
    #stores the background sound level chosen by the user
    global SoundLevel
    SoundLevel=request.get_json()
    print(SoundLevel)
    return "Successful"

@app.route('/RecordingButton',methods=['POST'])
def RecordingButton():
    #gets the value of the key the user pressed and saves it
    global Rvalue
    Rvalue=request.get_json()
    return "Successful"

@app.route('/StoppingButton',methods=['POST'])
def StoppingButton():
    #gets the value of the key the user pressed and saves it
    global Svalue
    Svalue=request.get_json()
    return "Successful"

@app.route("/getData",methods=["POST"])
def getData():
    #saves the data typed by the user into the document
    global Data
    Data=request.get_json()
    print(Data)
    return "Successful"

@app.route("/recordPause",methods=["POST"])
def recordPause():
    #records a pause
    RecordingDevice=continuousRecordingHopefully.Recorder() #initiates a new instance of the recorder object
    RecordingDevice.PauseSound()
    return jsonify("Successful")

@app.route("/recordEar",methods=["POST"])
def recordEar():
    #records the sound "ear"
    RecordingDevice=continuousRecordingHopefully.Recorder() #initiates a new instance of the recorder object
    RecordingDevice.earSound()
    return jsonify("Successful")
app.run(host="0.0.0.0",port=80)


# database=sqlite3.connect("frequencies.db")
# cur=database.cursor()
# # for x in alphabet:
# #     cur.execute("""INSERT INTO Phonemes(Spelling) VALUES(?)""",x)
# # database.commit()
# # database.close()
# # database.execute("""INSERT INTO Connection(SoundID, FrequencyID) VALUES(?,?)""",("A",340))
# # Data=database.execute("""SELECT * FROM Connection""").fetchall()
# # database.commit(
# # print(Data)
# # database.close()
# #database.execute("""DROP TABLE Phonemes""")
# #database.execute("""CREATE TABLE IF NOT EXISTS Phonemes(SoundID text NOT NULL PRIMARY KEY,Spelling text)""")
# for x in alphabet:
#     database.execute("""INSERT INTO Phonemes(SoundID,Spelling) Values(?,?)""",(x,x))
# database.commit()
# database.close()

# db=sqlite3.connect("frequencies.db")
# cur=db.cursor()
# db.execute("""drop table Phonemes""")
# db.commit()
# db.close()
# db.execute("""create table if not exists Phonemes (Phoneme varChar PRIMARY KEY,Spelling varChar)""")
# for x in phonemes:
#     for y in range(10):
#         db.execute("""INSERT or ignore INTO Frequencies(Letter) VALUES(?)""",("{}".format(x),))
# test=db.execute("""select Letter from Phonemes inner join Frequencies on Phonemes.Phoneme = Frequencies.Letter """).fetchall()
# print(test)
# db.commit()
# db.close()

#take in function from other script to get 10 most prominent frequencies.
#also take in function that records until no more sound.
#use the first one the second and get our phoneme frequencies.


# db=sqlite3.connect("frequencies.db")
# # print(db.execute("""select Letter from Frequencies where frequency == (?) and Prominence == (?)""",("{}".format(100.0),"{}".format(1))).fetchall()[0][0])
# PhonemeFreqs=[100,49,0,0,0,0,0,0,0,0]
# Score=[]
# number=0
# def comparing(db,freqs,Score,number):
#     current=freqs[number]
#     index=0
#     priority=db.execute("""select Frequency from Frequencies where Prominence == (?)""",("{}".format(number+1),)).fetchall()
#     id=db.execute("""select id from Frequencies where Prominence == (?)""",("{}".format(number+1),)).fetchall()
#     variance=float("inf")
#     for x in range(len(priority)):
#         try:
#             if abs((priority[x][0]-current)/priority[x][0]) <=variance:
#                 variance=abs((priority[x][0]-current)/priority[x][0])
#                 index=id[x][0]
#         except:
#             pass
#     try:
#         Phoneme=db.execute("""select Letter from Frequencies where id==(?)""",("{}".format(index))).fetchall()[0][0]
#     except:
#         Phoneme=None
#     Score.append((1-variance,Phoneme))
#     if number<9:
#         return comparing(db,freqs,Score,number+1)
#     else:
#         return Score

# Score=comparing(db,PhonemeFreqs,Score,number)
# print(Score)

# def counting(Score):
#     Phonemes={}
#     for x in range(len(Score)):
#         if Score[x][-1] not in Phonemes.keys():
#             Phonemes[Score[x][-1]]=Score[x][0]
#         else:
#             Phonemes[Score[x][-1]]=Phonemes[Score[x][-1]]+Score[x][0]
#     largest=max(Phonemes.values())
#     for x in Phonemes.keys():
#         if Phonemes[x]==largest:
#             return x
# Phoneme=counting(Score)
# print(Phoneme)
# db.close()

