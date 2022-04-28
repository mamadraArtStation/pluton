# coding=utf-8
import json


client=None

def init():
    with open('./config.json', 'r') as file:
        global config
        config = json.load(file)




