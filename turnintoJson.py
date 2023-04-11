import json
import pika
import sys
import re

Location1 = {
  "LocationID": 1,
  "City": "New York City",
  "Country": "United States",
  "Continent": "North America"
}
Location2 = {
  "LocationID": 2,
  "City": "Tokyo",
  "Country": "Japan",
  "Continent": "Asia"
}
Location3 = {
  "LocationID": 3,
  "City": "London",
  "Country": "United Kingdom",
  "Continent": "Europe"
}
Location4 = {
  "LocationID": 4,
  "City": "Los Angeles",
  "Country": "United States",
  "Continent": "North America"
}
Location5 = {
  "LocationID": 5,
  "City": "Cairo",
  "Country": "Egypt",
  "Continent": "Africa"
}
Location6 = {
  "LocationID": 6,
  "City": "Paris",
  "Country": "France",
  "Continent": "Europe"
}
node1 ={
  "nodeNum": 1
}
node2 = {
  "nodeNum": 2
}
node3= {
  "nodeNum": 3
}
node4 ={
  "nodeNum": 4
}
node5 = {
  "nodeNum": 5
}
node6 ={
  "nodeNum": 6
}
nodepaths1 ={
  "nodeNum": 1,
  "endNode": 3,
  "pathTime": 1468800,
  "pathWeight": 110000000,
  "pathType": "Ship"
}
nodepaths2 = {
  "nodeNum": 1,
  "endNode": 3,
  "pathTime": 1468800,
  "pathWeight": 110000000,
  "pathType": "Ship"
}
nodepaths3 = {
  "nodeNum": 3,
  "endNode": 6,
  "pathTime": 4500,
  "pathWeight": 5000,
  "pathType": "Plane"
}
nodepaths4= {
  "nodeNum": 2,
  "endNode": 5,
  "pathTime": 1468800,
  "pathWeight": 110000000,
  "pathType": "Ship"
}
nodepaths5 ={
  "nodeNum": 1,
  "endNode": 4,
  "pathTime": 281700,
  "pathWeight": 12500000,
  "pathType": "Train"
}