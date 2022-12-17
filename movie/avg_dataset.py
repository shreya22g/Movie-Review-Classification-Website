import pymongo
client=pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb=client.MovieDataBase
info=mydb.home_review
information=mydb.avgcollection
               
cursor = info.find({})
for r in cursor:
     name=r['movie_name']
     temp=0
     count=0
     moviename=0
     avg=0
     cursortwo = info.find({'movie_name':name})
     for r in cursortwo:
               temp=temp+r["review_score"]
               moviename=r["movie_name"]
               count=count+1
               avg= temp/count


     if(information.find({'moviename':moviename})==True):
               information.update(
                    {'moviename': moviename },
                    { "$set" :{'averagerating' : avg},
                    "$currentDate":{"lastmodified":True}}
               )
     else:
               information.delete_one({"moviename" : moviename})
               record={
               'moviename': moviename,
               'averagerating': avg
               }
               information.insert_one(record)