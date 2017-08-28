# -*- coding: utf-8 -*-
"""
Tool to import a CSV file containing watched show episodes and movies to Trakt.
"""
import logging
logging.basicConfig(format="%(asctime)s|%(levelname)8s|%(module)10s|%(funcName)10s|%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
from trakt import Trakt
import csv
import argparse
import pickle

version = "0.0.1"
oauth_cache_filename = "oauth.pkl"

Trakt.configuration.defaults.client(
	id='f8179920c5f5a00bf1408b39e8d3acd932846867f1fef008541b2c7726ccf944',
	secret='95cd2bae3c6a1175771af96329b3a11c03b943aa13448a56f812481d0af7c1b8'
)

def authenticate():
	"""
	Authenticate to the Trakt API using oauth.
	The oauth authentication token is saved for future usage.
	"""
	def authenticate():
		# Configure Application ID/Secret for ImporterForTrakt
		Trakt.configuration.defaults.client(
			id='f8179920c5f5a00bf1408b39e8d3acd932846867f1fef008541b2c7726ccf944',
			secret='95cd2bae3c6a1175771af96329b3a11c03b943aa13448a56f812481d0af7c1b8'
		)
		logger.info("Initialising authentication with Trakt.tv")
		print("In a browser, navigate to;\n{url}\nand enter the code below;".format(url=Trakt['oauth'].authorize_url('urn:ietf:wg:oauth:2.0:oob')))
		code = input("Authorization code:")
		
		if not code:
			print("Code not supplied")
			logger.error("Code not supplied")
			exit(1)
			
		authorisation = Trakt['oauth'].token(code, 'urn:ietf:wg:oauth:2.0:oob')
		if not authorisation:
			print("Invalid authorisation, please retry.")
			logger.error("Invalid authorisation")
			exit(1)
			
		logger.info("Authorisation successful")
		logger.debug("Authorisation: {authorisation}".format(authorisation=authorisation))
		try:
			with open(oauth_cache_filename, 'wb') as oauth_cache_file:
				pickle.dump(authorisation, oauth_cache_file)
		except:
			logger.error("Error when writing oauth cache {filename}".format(filename=oauth_cache_filename))
			exit(1)
		return authorisation
	
	def cache_load():
		"""
		Attempt to load the authentication token from a file.
		Perform full authentication if loading of the file fails.
		The validity of the authentication token is *NOT* checked.
		"""
		try:
			with open(oauth_cache_filename, 'rb') as oauth_cache_file:
				authorisation = pickle.load(oauth_cache_file)
				logger.info("Authenticated using cached credentials")
		except (EnvironmentError, EOFError):
			logger.error("Error whilst loading from oauth cache {filename}. Performing authentication.".format(filename=oauth_cache_filename))
			authorisation = authenticate()
		return authorisation
	
	authorisation = cache_load()
	return authorisation

def csv_to_objects(csvfile_path):
	"""
	Read a CSV file and convert it to a Python dictionary.
	
	Parameters
	----------
	csvfile_path : string
								 The absolute or relative path to a valid CSV file.
	
	Returns
	-------
	dict
		A dict containing a dict of show/episode entries and a dict of movie entries.
	"""
	logger.info("Attempting to read from {file}".format(file=csvfile_path))
	try:
		with open(csvfile_path) as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',')
			headers = next(csvreader)
			shows = []
			movies = []
			for row in csvreader:
				item = {}
				for header_num, header in enumerate(headers):
					item[header] = row[header_num]
				logger.debug(item)
				if item['type'] == "episode":
					shows.append(item)
				elif item['type'] == "movie":
					movies.append(item)
				else:
					logger.error("Unknow item type {type}".format(type=item['type']))
					exit(1)
			logger.info("{shows} shows and {movies} movies read from CSV".format(shows=len(shows), movies=len(movies)))
	except (EnvironmentError, EOFError):
		logger.error("Error whilst loading CSV file {filename}".format(filename=csvfile_path))
	return {'shows': shows, 'movies': movies}

def add_item_to_history(item, type):
	"""
	Add a single item extracted from the CSV file to the user's Trakt history.
	
	Parameters
	----------
	item : dict
				 An item dict extracted from the CSV file.
	type : string
				 The type of item, valid values are 'show' or 'movie'
	"""
	if type == 'show':
		media_object = {
			'episodes': [
				{
					"watched_at": item['watched_at'],
					"ids": {
						"trakt": item['episode_trakt_id']
					}
				}
			]
		}
	elif type == 'movie':
		media_object = {
			'movies': [
				{
					"watched_at": item['watched_at'],
					"ids": {
						"trakt": item['trakt_id']
					}
				}
			]
		}
	else:
		logger.error("Invalid type {type}".format(type=type))
	with Trakt.configuration.oauth.from_response(authorisation):
		with Trakt.configuration.http(retry=True):
			result = Trakt['sync/history'].add(media_object)
			logger.debug(result)

def add_items_to_history(items):
	"""
	Add a number of items extracted from the CSV file to the user's Trakt history.
	Parameters
	----------
	items : dict
					An dict of show and movie items extracted from the CSV file.	
	"""
	shows = items['shows']
	movies = items['movies']
	for item in shows:
		add_item_to_history(item, type='show')
	for item in movies:
		add_item_to_history(item, type='movie')

def main():
	parser = argparse.ArgumentParser(description='Import a CSV file containing TV and Movie watch history to Trakt.')
	parser.add_argument('--file', help="Path to the CSV file to import", required=True)
	args = parser.parse_args()
	print("Importer for Trakt, version {version}".format(version=version))
	global authorisation
	authorisation = authenticate()
	items = csv_to_objects(args.file)
	add_items_to_history(items)

if __name__ == "__main__":
	main()