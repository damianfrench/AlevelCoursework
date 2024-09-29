import sqlite3

def Database(number):
    #returns an array of symbols and frequencies depending on the desired level of prominence which is passed as a parameter.
    db=sqlite3.connect("/Users/damianjoshuafrench/Desktop/coursework-1/frequencies.db")
    temp=db.execute("""select Letter,Frequency from Frequencies where Prominence == (?)""",("{}".format((number+1)),)).fetchall()
    db.close()
    return temp

def Comparing(recorded,freqs):
    difference=[]
    #array to store percentage differences
    for freq in freqs:
                #loops through frequencies from database
        try:
            if recorded-freq[-1]>0:
                P=((recorded-freq[-1])/freq[-1])*100
                # difference.append((P,db.execute("""select spelling from Phonemes where Phonemes == (?)""",("{}".format(freq[0]))).fetchall()))
                difference.append((P,freq[0]))
                #calculates percentage difference and adds it to the array "difference"
            else:
                P=((freq[-1]-recorded)/freq[-1])*100
                difference.append((P,freq[0]))
                # difference.append((P,db.execute("""select spelling from Phonemes where Phonemes == (?)""",("{}".format(freq[0]))).fetchall()))
                #calculates percentage difference and adds it to the array "difference"
        except:
            pass
            #try except used in case of missing data in database
    return difference


# Comparing(98,Database(1))

def adding(Hf):
    db=sqlite3.connect("/Users/damianjoshuafrench/Desktop/coursework-1/frequencies.db")
    # for x in range(len(Hf)):
    #     db.execute("""insert into Frequencies(Frequency) Values(?) where Prominence==(?)""",(Hf[x],(x+1)),)
    #need to specify what phoneme we are currently recording, possibly by having the program loop through and choose a specific one
    #recording them should be ok as should only be one sound
    x="zh"
    print(x)
    for y in range(len(Hf)):
        db.execute("""Update Frequencies set Frequency=(?) where Prominence==(?) and Letter==(?)""",("{}".format(Hf[y]),(y+1),x,))
    db.commit()
    # print(db.execute("""select * from Frequencies where Letter==(?)""",("{}".format(x),)).fetchall())
    db.close()

def Pause(Hf):
    db=sqlite3.connect("/Users/damianjoshuafrench/Desktop/coursework-1/frequencies.db")
    for y in range(len(Hf)):
        db.execute("""Update Frequencies set Frequency=(?) where Prominence==(?) and Letter==(?)""",("{}".format(Hf[y]),(y+1),"pause",))
    db.commit()
    db.close()
def ear(Hf):
    db=sqlite3.connect("/Users/damianjoshuafrench/Desktop/coursework-1/frequencies.db")
    for y in range(len(Hf)):
        db.execute("""Update Frequencies set Frequency=(?) where Prominence==(?) and Letter==(?)""",("{}".format(Hf[y]),(y+1),"ear",))
    db.commit()
    db.close()