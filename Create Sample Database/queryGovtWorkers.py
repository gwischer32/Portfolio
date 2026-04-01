# queryGovtWorkers.py
import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient()      # defaults to localhost:27017
db = client.db_people
peeps = db.thePeople

pp = pprint.PrettyPrinter(indent=2)

# --------------------------
# Q1: Complete info about people who have 7 children
# --------------------------
print("\nQ1: Complete info about people who have 7 children")
q1 = peeps.find({"numChildren": 7})
for p in q1:
    pp.pprint(p)

# --------------------------
# Q2: pid, state, and name of children for people who have 7 children
# --------------------------
print("\nQ2: pid, state, and children names for people who have 7 children")
q2 = peeps.find(
    {"numChildren": 7},
    {"_id": 0, "pid": 1, "state": 1, "children": 1}
)
for p in q2:
    pp.pprint(p)

# --------------------------
# Q3: Complete info of people who live in CA and have 6 children
# --------------------------
print("\nQ3: People who live in CA and have 6 children")
q3 = peeps.find(
    {"state": "CA", "numChildren": 6}
)
for p in q3:
    pp.pprint(p)

# --------------------------
# Q4: Complete info of people who live in CA and have 6 or 7 children
# --------------------------
print("\nQ4: People who live in CA and have 6 or 7 children")
q4 = peeps.find(
    {"state": "CA", "numChildren": {"$in": [6, 7]}}
)
for p in q4:
    pp.pprint(p)

# --------------------------
# Q5: List pid and children names for people who have a child containing 'Bob A'
# --------------------------
print("\nQ5: People who have a child whose name contains 'Bob A'")
q5 = peeps.find(
    {"children": {"$regex": "Bob A"}},
    {"_id": 0, "pid": 1, "children": 1}
)
for p in q5:
    pp.pprint(p)

# --------------------------
# Q6: Aggregation – number of people who have 0, 1, ..., 8 children
# --------------------------
print("\nQ6: Number of people who have 0–8 children")
pipeline6 = [
    {"$group": {
        "_id": "$numChildren",
        "numInGroup": {"$sum": 1}
    }},
    {"$sort": {"_id": 1}}
]
for p in peeps.aggregate(pipeline6):
    pp.pprint(p)

# --------------------------
# Q7: Aggregation – average salary for each state
# --------------------------
print("\nQ7: Average salary for each state")
pipeline7 = [
    {"$group": {
        "_id": "$state",
        "avgSalary": {"$avg": "$salary"},
        "numInGroup": {"$sum": 1}
    }},
    {"$sort": {"_id": 1}}
]
for p in peeps.aggregate(pipeline7):
    pp.pprint(p)

# --------------------------
# Q8: Aggregation – average salary and count for WI
# --------------------------
print("\nQ8: Average salary and number of people in WI")
pipeline8 = [
    {"$match": {"state": "WI"}},
    {"$group": {
        "_id": "$state",
        "avgSalary": {"$avg": "$salary"},
        "numInGroup": {"$sum": 1}
    }}
]
for p in peeps.aggregate(pipeline8):
    pp.pprint(p)

# --------------------------
# Q9: Aggregation – average/min/max salary for Midwest states
# --------------------------
print("\nQ9: Average/min/max salary for Midwest states")
midwest_states = ["ND","SD","NE","KS","MN","IA","MS","WI","IL","IN","MI","OH"]

pipeline9 = [
    {"$match": {"state": {"$in": midwest_states}}},
    {"$group": {
        "_id": "$state",
        "avgSalary": {"$avg": "$salary"},
        "minSalary": {"$min": "$salary"},
        "maxSalary": {"$max": "$salary"},
        "numInGroup": {"$sum": 1}
    }},
    {"$sort": {"_id": 1}}
]
for p in peeps.aggregate(pipeline9):
    pp.pprint(p)

# --------------------------
# Q10: Aggregation – states with avg salary >= 82,000
# --------------------------
print("\nQ10: States where avg salary >= 82,000")
pipeline10 = [
    {"$group": {
        "_id": "$state",
        "avgSalary": {"$avg": "$salary"},
        "numInGroup": {"$sum": 1}
    }},
    {"$match": {"avgSalary": {"$gte": 82000}}},
    {"$sort": {"_id": 1}}
]
for p in peeps.aggregate(pipeline10):
    pp.pprint(p)

# --------------------------
# Q11: Aggregation – Midwest states whose avg salary > 82,000
# --------------------------
print("\nQ11: Midwest states whose avg salary > 82,000")
pipeline11 = [
    {"$match": {"state": {"$in": midwest_states}}},
    {"$group": {
        "_id": "$state",
        "avgSalary": {"$avg": "$salary"},
        "minSalary": {"$min": "$salary"},
        "maxSalary": {"$max": "$salary"},
        "numInGroup": {"$sum": 1}
    }},
    {"$match": {"avgSalary": {"$gt": 82000}}},
    {"$sort": {"_id": 1}}
]
for p in peeps.aggregate(pipeline11):
    pp.pprint(p)
