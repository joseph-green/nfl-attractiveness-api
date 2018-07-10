import sqlite3
import json

def db_connect():
    db_conn = sqlite3.connect('./nfl.db')
    db = db_conn.cursor()

    return db

def db_close(db_conn):
    
    #close the database
    db_conn.close()

def get_player_by_id(player_id):

    db = db_connect()

    db.execute("""SELECT * FROM players WHERE player_id=?""", (player_id,))

    player = db.fetchone()

    keys = [des[0] for des in db.description]

    db_close(db)

    if player:
    	return parse_json(player,keys)
    else:
    	return "No results were found"

def get_player_by_name(last_name,first_name=None):

    db = db_connect()
    
    #if a first name is given, search using first and last names, otherwise just by last name
    if first_name:
        db.execute("""SELECT * FROM players WHERE player_first_name=? AND player_last_name=?""", (first_name,last_name))
    else:
        db.execute("""SELECT * FROM players WHERE player_last_name=?""", (last_name,))

    players = db.fetchall()

    db_close(db)

    #if no players are found, return an error
    if len(players) == 0:
        return "No results were found"
    #if a single player is found, return that player
    elif len(players) == 1:
        return parse_json(players[0])
    else:
        for player in players:
        	player = parse_json(player)

        return players
    

    



def parse_json(response,columns):

	response_hash = {}

	for i in range(0,len(response)):
		response_hash[columns[i]] = response[i]

	return json.dumps(response_hash)

