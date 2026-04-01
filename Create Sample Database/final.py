import pymongo

import numpy as np

from pymongo import MongoClient

 

client = MongoClient() # connects on default host

db = client.db_temp

db.people.drop()

 

 

states = ["AL","AK","AZ","AZ","CA","CO"]

fNames = ["Bob","Mary","Isabella","Santiago","Valentina"]

mNames = ["A","B","C","D","E","F"]

lNames = ["Garcia","Martinez","Baker","Jackson","Brown","Smith"]

 

numDocs = 100

for i in range(0,numDocs):

    aPid = i

aFName = fNames[ np.random.randint(len(fNames)) ]

aMName = mNames[ np.random.randint(len(mNames)) ]

aLName = lNames[ np.random.randint(len(lNames)) ]

aName = aFName + " " + aMName + " " + aLName

aAge = np.random.randint(100) + 18

aHeight = np.random.randint(150,200) # in centimeters

aBirth = 2019 - aAge

aSalary = np.random.randint(100000) + 30000 # lowest paid is 30K

aState = states[ np.random.randint( len(states) ) ]

newPerson = {"pid":aPid,"firstName":aFName, "MI":aMName,

"lastName":aLName, "state":aState, "age":aAge,"birth":aBirth,

"salary":aSalary, "height":aHeight}

db.people.insert_one(newPerson)

