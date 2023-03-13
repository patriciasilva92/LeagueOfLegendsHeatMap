import requests, time


def getSummonerId(name):
	# username : the username used by the player to sign onto League of Legends
	#
	# returns : summonerId , id number corresponding to given username

	# get summoner ID
	url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + '?api_key=RGAPI-74c2c1c6-0252-4ee0-8f7d-ac0a128f34fb'
	response = requests.get(url)
	response_json = response.json()
	#print("SummonerId: " + str(id))

	puuid = response_json['puuid']


	return puuid
	

def getMatchIds(puuid):
	# summonerId : id number for the given player username, use getSummonerId to get this value
	#
	# returns : matchIds , a list of all matchId numbers for every ranked game played by the player
	# get Match IDS
	url = 'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/' + str(puuid) + '/ids/?api_key=RGAPI-74c2c1c6-0252-4ee0-8f7d-ac0a128f34fb'
	response = requests.get(url)
	response_json = response.json()



	#print("Number of ranked matches played: " + str(len(matchIds)))

	return response_json
	

def getPositionData(matchIds, data):
	# matchIds : list of match Ids
	# data : list in which to put the data into (should be initialized in main() )
	#
	# returns : data  , a list containing all the position data for each player for every ranked game the player has played

	# Calculate runtime and set delay so too rate limit for API isn't exceeded
	delay = 1.5
	loopTime = 2
	timeToRun = len(matchIds) * ( delay + loopTime )
	print("Estimated time to run : " + str(timeToRun))

	# get position data [x,y] for every player for each match ID and append it to data list
	for matchId in matchIds:
		# build url for API request

		#print(matchId)
		url = 'https://europe.api.riotgames.com/lol/match/v5/matches/' + str(matchId) + '/timeline/?api_key=RGAPI-74c2c1c6-0252-4ee0-8f7d-ac0a128f34fb'
		#print(url)
		response = requests.get(url)
		response_json = response.json()
		#data.append('START OF MATCH: ' + str(matchId))

		# Getting errors on certain matches, use try to skip these. Not sure why but error will be given on different matches when script is rerun. 
		# Might be something to do with API server
		try: 

			for frame in response_json['info']['frames']:
				# sometimes the last frame of a game does not contain position data, use try for error checking
			    try:
				    data.append([frame['participantFrames']['1']['position']['x'] , frame['participantFrames']['1']['position']['y']])
				    data.append( [frame['participantFrames']['2']['position']['x'] , frame['participantFrames']['2']['position']['y'] ] )
				    data.append( [frame['participantFrames']['3']['position']['x'] , frame['participantFrames']['3']['position']['y'] ] )
				    data.append( [frame['participantFrames']['4']['position']['x'] , frame['participantFrames']['4']['position']['y'] ] )
				    data.append( [frame['participantFrames']['5']['position']['x'] , frame['participantFrames']['5']['position']['y'] ] )
				    data.append( [frame['participantFrames']['6']['position']['x'] , frame['participantFrames']['6']['position']['y'] ] )
				    data.append( [frame['participantFrames']['7']['position']['x'] , frame['participantFrames']['7']['position']['y'] ] )
				    data.append( [frame['participantFrames']['8']['position']['x'] , frame['participantFrames']['8']['position']['y'] ] )
				    data.append( [frame['participantFrames']['9']['position']['x'] , frame['participantFrames']['9']['position']['y'] ] )
				    data.append( [frame['participantFrames']['10']['position']['x'] , frame['participantFrames']['10']['position']['y'] ] )
			    except KeyError:
			    	continue

		except KeyError:
			continue

		# delay loop so API request limit is not exceeded
		time.sleep(delay)

	return data

def writeToFile(data):
	# writes the data to file
	# data : list containing all position data
	#
	# creates a text file with the data in the same directory as the script
	textFile = open("heatMapData.txt", "w")
	for item in data:
		textFile.write(str(item[0]))
		textFile.write(',')
		textFile.write(str(item[1]))
		textFile.write("\n")
	textFile.close()


def main():
	name = 'Acroda92'
	puuid = getSummonerId(name)
	matchIds = getMatchIds(puuid)
	#testMatchIds = matchIds[0:15]
	#print(matchIds)
	data = []
	data = getPositionData(matchIds, data)
	writeToFile(data)
	


main()