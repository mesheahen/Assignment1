# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 10:21:57 2015

@author: mariah
"""
from geopy.distance import vincenty
import sqlite3

#import the database, establish a connection
conn = sqlite3.connect("renewable.db")
c = conn.cursor()

#import data from files and create lists for data, this way we can more easily 
#work with data. The following four lines are importing Latitude data from
#the Location table and creating a list of that data.
c.execute("SELECT lat FROM location;")
Plant_Latitude = []
for item in c:
    Plant_Latitude.append(float(item[0]))

#the following four lines are importing Longitude data from the Location table
#and creating a list.
c.execute("SELECT long FROM location;")
Plant_Longitude = []
for item in c:
    Plant_Longitude.append(float(item[0]))

#the following six lines are importing Producation data from the Location table
#and creating a list. also, here we are standardizing production data to a
#number of monthly hauls trucks would have to carry along the roads.
#we do this by defining months as 12 and an arbitrary number of tons possible
#to carry per month between locations. We are then rounding this number to 
#an integer.
Months = 12
Tonnage = 30
c.execute("SELECT production FROM location;")
Plant_Production = []
for item in c:
    Plant_Production.append(int(float(item[0])/(Months*Tonnage)))
    
#The following five lines are summing the production data from the Location 
#table. By multiplying this number by a production rate, and then
#dividing by the months and tons we've declared above, we will get our 
#expected number of hauls we would need on a monthly basis between locations.
#Here we are also rounding to the closest int.
Production_Rate=0.5
c.execute("SELECT sum(production) FROM location;")
End_Product = []
for item in c:
    End_Product.append(int((float(item[0])*(Production_Rate)))/(Months*Tonnage))    

#the following four lines are importing Latitude data from the Ports table
#and creating a list.
c.execute("SELECT lat FROM ports;")
Port_Latitude = []
for item in c:
    Port_Latitude.append(float(item[0]))

#the following four lines are importing Longitude data from the Ports table
#and creating a list.
c.execute("SELECT long FROM ports;")
Port_Longitude = []
for item in c:
    Port_Longitude.append(float(item[0]))

#First function created is to establish a measured distance between a certain
#location and all other locations of raw materials. Each distance is then
#multiplied by our Plant_Production. Plant_Production defines the number
#of hauls we need. Then we append this list to our new list, Plant_Distance.
i=0
j=0
Plant_Distance = []
for j in range(len(Plant_Latitude)):
        result = 0
        for i in range(len(Plant_Latitude)):
            start = (Plant_Latitude[int(i)], Plant_Longitude[int(i)])
            finish = (Plant_Latitude[int(j)], Plant_Longitude[int(j)])
            equa = vincenty(start, finish).kilometers
            solution = equa * Plant_Production[i]
            result = result + solution
            i += 1
        Plant_Distance.append(result)
        j += 1

#create a function to measure the distance between a location given in the
#locations table and a port location given in the Ports table. This distance
#is then mutlipled by End_Product which is our number of trips/hauls we need
#in order to carry all our end products from the to be selected Plant location
#to the to be selected Port location. We then append this to our new list 
#called Port_Distance.
i=0
j=0
Port_Distance = []
for j in range(len(Plant_Latitude)):
        for i in range(len(Port_Latitude)):
            Plant = (Plant_Latitude[int(j)], Plant_Longitude[int(j)])
            Port = (Port_Latitude[int(i)], Port_Longitude[int(i)])
            equa = vincenty(Plant, Port).kilometers
            solution = equa * End_Product[0]
            Port_Distance.append(solution)
        i += 1
        j += 1
        
#create a function to calculate the Total_Distance that our trucks will
#travel between our chosen Plant location(x) and our chosen Port location(y).        
#We sum the distance between x and y, and then we sum all distance we need
#between all other raw material locations to converge together at the chosen
#Plant location.
x=0
y=3
f=0
z=0
count=0
Total_Distance = []
while z != len(Port_Distance):
    if count != 3:
        for i in Port_Distance[x:y]:
            a = i + Plant_Distance[f]
            Total_Distance.append(a)
            count += 1
    else:
        x += 3
        y += 3
        f += 1
        count = 0
        z += 3 
        
#create a function to find distance between Plant and Port that will return to
#us the least amount of km's trucks have to haul possible on a monthly basis.
list1 = []
g=0
count=0
while g != len(Total_Distance):
    if count != len(Port_Latitude):
        for i in range(len(Port_Latitude)):
            list1.append(i)
            count += 1
    else:
        count = 0
        g += 1 

#Formulating end product to this problem.
l = min(Total_Distance)
z = Total_Distance.index(l)
f = len(Port_Latitude)
k = int(z/f)
p = list1[z]

print "The most efficient location to create a new Plant "
print "is the number/location ", k ," from our list. "
print "This is keeping in mind that our list begins at 0. " 
print "Again, our list comes from the given database called " 
print "Renewable. The most efficient Port location"
print "is the number/location ", p ," " 
print "Again, keeping in mind our list begins at 0. "
print "Again, our list comes from the given database Renewable."
print z
print f
print k
print p
print l 