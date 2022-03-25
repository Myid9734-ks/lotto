import requests
import sqlite3
import random
import time

a = [1,2,3,4]
b = [1,2,5,6]


set1 = set(a) & set(b)
set1 = list(set1)
print(set1)
print(len(set1))