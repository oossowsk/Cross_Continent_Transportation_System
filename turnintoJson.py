import json
import pika
import sys
import re

Location1 = {
  "LocationID": 0,
  "City": "New York City",
  "Country": "United States",
  "Continent": "North America"
}
Location2 = {
  "LocationID": 1,
  "City": "Tokyo",
  "Country": "Japan",
  "Continent": "Asia"
}
Location3 = {
  "LocationID": 2,
  "City": "London",
  "Country": "United Kingdom",
  "Continent": "Europe"
}
Location4 = {
  "LocationID": 3,
  "City": "Los Angeles",
  "Country": "United States",
  "Continent": "North America"
}
Location5 = {
  "LocationID": 4,
  "City": "Cairo",
  "Country": "Egypt",
  "Continent": "Africa"
}
Location6 = {
  "LocationID": 5,
  "City": "Paris",
  "Country": "France",
  "Continent": "Europe"
}
node0 ={
  "nodeNum": 0
}
node1 = {
  "nodeNum": 1
}
node2= {
  "nodeNum": 2
}
node3 ={
  "nodeNum": 3
}
node4 = {
  "nodeNum": 4
}
node5 ={
  "nodeNum": 5
}
nodepaths0 ={
  "nodeNum": 0,
  "endNode": 2,
  "pathTime": 1468800,
  "pathWeight": 110000000,
  "pathType": "Ship"
}
nodepaths1 = {
  "nodeNum": 0,
  "endNode": 2,
  "pathTime": 1468800,
  "pathWeight": 110000000,
  "pathType": "Ship"
}
nodepaths2 = {
  "nodeNum": 2,
  "endNode": 5,
  "pathTime": 4500,
  "pathWeight": 5000,
  "pathType": "Plane"
}
nodepaths3= {
  "nodeNum": 1,
  "endNode": 4,
  "pathTime": 1468800,
  "pathWeight": 110000000,
  "pathType": "Ship"
}
nodepaths4 ={
  "nodeNum": 0,
  "endNode": 3,
  "pathTime": 281700,
  "pathWeight": 12500000,
  "pathType": "Train"
}
nodepaths5 ={
  "nodeNum": 3,
  "endNode": 1,
  "pathTime": 950400,
  "pathWeight": 110000000,
  "pathType": "Ship"
}
nodepaths6 ={
  "nodeNum": 4,
  "endNode": 5,
  "pathTime": 17100,
  "pathWeight": 5000,
  "pathType": "Plane"
}
nodepaths7 ={
  "nodeNum": 5,
  "endNode": 1,
  "pathTime": 29700,
  "pathWeight": 5000,
  "pathType": "Plane"
}