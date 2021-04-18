from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import json
import pprint

key = "ef0f49cc4f747effb674303a7c49e03a"
url = "https://api.themoviedb.org/"
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
@cross_origin(allow_headers=['Content-Type'])
def index():
	return app.send_static_file('index.html')


@app.route("/trending", methods = ['GET'])
@cross_origin(allow_headers=['Content-Type'])
def trending():
	trending = "https://api.themoviedb.org/3/trending/movie/week?api_key=ef0f49cc4f747effb674303a7c49e03a"
	trending_values = requests.get(trending).content
	trending_data = json.loads(trending_values.decode('utf-8'))
	results = trending_data['results']
	trending_arr=[]
	if results:
		new_results = results[:5]
		for res in new_results:
			trending_dict = {}
			if 'title' in res:
				title = res['title']
				trending_dict['title'] = title

			if 'backdrop_path' in res:
				backdrop_url = "https://image.tmdb.org/t/p/w780"
				# movies_dict['poster_path'] = poster_url+poster_path
				backdrop_path = res['backdrop_path']
				trending_dict['backdrop_path'] = backdrop_url+backdrop_path

			if 'release_date' in res:
				if res['release_date']:
					release_date = res['release_date']
					trending_dict['release_date'] = release_date	
				else:
					trending_dict['release_date'] = "N/A"	

			trending_arr.append(trending_dict)
	return jsonify(trending_arr)


@app.route("/airing",methods = ['GET'])
@cross_origin(allow_headers=['Content-Type'])
def airing():
	airing = "https://api.themoviedb.org/3/tv/airing_today?api_key=ef0f49cc4f747effb674303a7c49e03a"
	airing_values = requests.get(airing).content
	airing_data = json.loads(airing_values.decode('utf-8'))
	airing_results = airing_data['results']
	# pprint.pprint(airing_results)
	airing_arr=[]
	if airing_results:
		new_results = airing_results[:5]
		for result in new_results:
			airing_dict = {}
			if 'id' in result:
				id = result['id']
				airing_dict['id'] = id

			if 'name' in result:
				name = result['name']
				airing_dict['name'] = name

			if 'overview' in result:
				if result['overview']:
					overview = result['overview']
					airing_dict['overview'] = overview	
				else:
					airing_dict['overview'] = "N/A"
			
			if 'backdrop_path' in result:
				backdrop_url = "https://image.tmdb.org/t/p/w780"
				backdrop_path = result['backdrop_path']
				
				if backdrop_path:
					airing_dict['poster_path'] = backdrop_url + backdrop_path
				else:
					airing_dict['poster_path'] = "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg"
				

			if 'first_air_date' in result:
				if result['first_air_date']:
					first_air_date = result['first_air_date']
					airing_dict['first_air_date'] = first_air_date
				else:
					airing_dict['first_air_date'] = "N/A"

			if 'vote_average' in result:
				vote_average = result['vote_average']
				airing_dict['vote_average'] = vote_average	
			
			if 'vote_count' in result:
				vote_count = result['vote_count']
				airing_dict['vote_count'] = vote_count
			
			if 'genre_ids' in result:
				if result['genre_ids']:
					genre_ids = result['genre_ids']
					airing_dict['genre_ids'] = genre_ids
				else:
					airing_dict['genre_ids'] = "N/A"
				

			airing_arr.append(airing_dict)

	return jsonify(airing_arr)

@app.route("/showMore", methods = ['GET'])
@cross_origin(allow_headers=['Content-Type'])
def showMore():
	id = request.args.get("id")
	category_name = request.args.get("category_name")
	show_more_array = []
	if category_name == "movie":
		#for content
		content_url = "https://api.themoviedb.org/3/movie/"+str(id)+"?api_key=ef0f49cc4f747effb674303a7c49e03a&language=en-US"
		show_more_content = requests.get(content_url).content
		content_data = json.loads(show_more_content.decode('utf-8'))
		content_dict = {}
		if 'id' in content_data:
			id = content_data['id']
			content_dict['id'] = id
		
		if 'overview' in content_data:
			if content_data['overview']:
				overview = content_data['overview']
				content_dict['overview'] = overview
			else:
				content_dict['overview'] = "N/A"

		if 'title' in content_data:
			title = content_data['title']
			content_dict['title'] = title

		if 'runtime' in content_data:
			runtime = content_data['runtime']
			content_dict['runtime'] = runtime
		
		if 'release_date' in content_data:
			if content_data['release_date']:
				release_date_list = content_data['release_date'].split('-')
				release_date = release_date_list[0]
				content_dict['release_date'] = release_date
			else:
				content_dict['release_date'] = "N/A"

		if 'spoken_languages' in content_data:
			spoken_languages = content_data['spoken_languages']
			spoken_list = []
			for languages in spoken_languages:
				spoken_list.append(languages["english_name"])
			spoken_str = ', '.join(spoken_list)
			if len(spoken_str) == 0:
				content_dict['spoken_languages'] = "N/A"
			else:
				content_dict['spoken_languages'] = spoken_str

		if 'vote_average' in content_data:
			vote_average = content_data['vote_average']
			content_dict['vote_average'] = str(vote_average/2)

		if 'vote_count' in content_data:
			vote_count = content_data['vote_count']
			content_dict['vote_count'] = vote_count

		if 'poster_path' in content_data:
			poster_url = "https://image.tmdb.org/t/p/w500"
			poster_path = content_data['poster_path']
			if poster_path:
				content_dict['poster_path'] = poster_path
			else:
				content_dict['poster_path'] = "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg"

		if 'backdrop_path' in content_data:
			backdrop_url = "https://image.tmdb.org/t/p/w780"
			backdrop_path = content_data['backdrop_path']
			if backdrop_path:
				content_dict['backdrop_path'] = backdrop_url+backdrop_path
			else:
				content_dict['backdrop_path'] = "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg"

		if 'genres' in content_data:
			if content_data['genres']:
				genres = content_data['genres']
				genres_list = []
				for genre in genres:
					genres_list.append(genre['name'])
				genre_str = ', '.join(genres_list)
				content_dict['genres'] = genre_str
			else:
				content_dict['genres'] = "N/A"
				

		#for cast
		cast_url = "https://api.themoviedb.org/3/movie/"+str(id)+"/credits?api_key=ef0f49cc4f747effb674303a7c49e03a&language=en-US"
		show_more_cast = requests.get(cast_url).content
		cast_data = json.loads(show_more_cast.decode('utf-8'))
		cast_val = cast_data['cast']
		cast_values = []
		cast_data = cast_val[:8]
		for cast in cast_data:
			cast_dict = {}
			if 'name' in cast:
				name = cast['name']
				cast_dict['name'] = name
			
			if 'profile_path' in cast:
				profile_url = "https://image.tmdb.org/t/p/w185"
				profile_path  = cast['profile_path']
				if profile_path:
					cast_dict['profile_path'] = profile_url + profile_path 
				else:
					cast_dict['profile_path'] = "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/person-placeholder.png"
				

			if 'character' in cast:
				if cast['character']:
					character = cast['character']
					cast_dict['character'] = character
				else:
					cast_dict['character'] = "N/A"
			
			cast_values.append(cast_dict)

		#for reviews
		review_url = "https://api.themoviedb.org/3/movie/"+str(id)+"/reviews?api_key=ef0f49cc4f747effb674303a7c49e03a&language=en-US&page=1"
		show_more_review = requests.get(review_url).content
		review_data = json.loads(show_more_review.decode('utf-8'))
		review_val = review_data['results']
		# pprint.pprint(review_val)
		# review_data = review_data[:5]
		review_values = []
		for review in review_val[:5]:
			reviews_dict = {}
			if 'username' in review['author_details']:
				# print("username")
				# username_details = review['author_details']
				username = review['author_details']['username']
				# print(username)
				reviews_dict['username'] = username

			if 'content' in review:
				content = review['content']
				reviews_dict['content'] = content
			
			if 'rating' in review['author_details']:
				# rating_details = review['author_details']
				rating = review['author_details']['rating']
				reviews_dict['rating'] = rating

			if 'created_at' in review:
				if review['created_at']:
					created_at_string = review['created_at'].split('T')[0]
					list_created_at=created_at_string.split('-')
					created_at=list_created_at[1]+'/'+list_created_at[2]+'/'+list_created_at[0]
					reviews_dict['created_at'] = created_at
				else:
					reviews_dict['created_at'] = "N/A"

			review_values.append(reviews_dict)

		show_more_array.append(content_dict)
		show_more_array.append(cast_values)
		show_more_array.append(review_values)
		
	elif category_name == "show":
		#for tv shows content"
		content_url = "https://api.themoviedb.org/3/tv/"+str(id)+"?api_key=ef0f49cc4f747effb674303a7c49e03a&language=e n-US"
		show_more_content = requests.get(content_url).content
		content_data = json.loads(show_more_content.decode('utf-8'))
		content_dict = {}
		if 'backdrop_path' in content_data:
			backdrop_url = "https://image.tmdb.org/t/p/w780"
			backdrop_path = content_data['backdrop_path']
			if backdrop_path:
				content_dict['backdrop_path'] = backdrop_url+backdrop_path
			else:
				content_dict['backdrop_path'] = "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg"

		if 'episode_run_time' in content_data:
			episode_run_time = content_data['episode_run_time']
			content_dict['episode_run_time'] = episode_run_time

		if 'first_air_date' in content_data:
			if content_data['first_air_date']:
				first_air_date_list = content_data['first_air_date'].split('-')
				first_air_date = first_air_date_list[0]
				content_dict['first_air_date'] = first_air_date
			else:
				content_dict['first_air_date'] = "N/A"
		
		if 'genres' in content_data:
			if content_data['genres']:
				genres = content_data['genres']
				genres_list = []
				for genre in genres:
					genres_list.append(genre['name'])
				genre_str = ', '.join(genres_list)
				content_dict['genres'] = genre_str
			else:
				content_dict['genres'] = "N/A"
		
		if 'id' in content_data:
			id = content_data['id']
			content_dict['id'] = id
		
		if 'name' in content_data:
			name = content_data['name']
			content_dict['name'] = name

		if 'number_of_seasons' in content_data:
			number_of_seasons = content_data['number_of_seasons']
			content_dict['number_of_seasons'] = number_of_seasons
		
		if 'overview' in content_data:
			if content_data['overview']:
				overview = content_data['overview']
				content_dict['overview'] = overview
			else:
				content_dict['overview'] = "N/A"

		if 'poster_path' in content_data:
			poster_url = "https://image.tmdb.org/t/p/w500"
			poster_path = content_data['poster_path']
			content_dict['poster_path'] = poster_path
			if poster_path:
				content_dict['poster_path'] = poster_url + poster_path
			else:
				content_dict['poster_path'] = "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg"

		if 'spoken_languages' in content_data:
			spoken_languages = content_data['spoken_languages']
			spoken_list = []
			for languages in spoken_languages:
				spoken_list.append(languages["english_name"])
			spoken_str = ', '.join(spoken_list)
			if len(spoken_str)==0:
				content_dict['spoken_languages'] = "N/A"
			else:
				content_dict['spoken_languages'] = spoken_str

		if 'vote_average' in content_data:
			vote_average = content_data['vote_average']
			content_dict['vote_average'] = str(vote_average/2)

		if 'vote_count' in content_data:
			vote_count = content_data['vote_count']
			content_dict['vote_count'] = vote_count
					

		#for tv shows cast
		cast_url = "https://api.themoviedb.org/3/tv/"+str(id)+"/credits?api_key=ef0f49cc4f747effb674303a7c49e03a&lang uage=en-US"
		show_more_cast = requests.get(cast_url).content
		cast_data = json.loads(show_more_cast.decode('utf-8'))
		cast_val = cast_data['cast']
		cast_values = []
		cast_data = cast_val[:8]
		for cast in cast_data:
			cast_dict = {}
			if 'name' in cast:
				name = cast['name']
				cast_dict['name'] = name
			
			if 'profile_path' in cast:
				profile_url = "https://image.tmdb.org/t/p/w185"
				profile_path  = cast['profile_path']
				if poster_path:
					cast_dict['profile_path'] = profile_url + profile_path 
				else:
					cast_dict['profile_path'] = "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/person-placeholder.png"
				
			if 'character' in cast:
				if cast['character']:
					character = cast['character']
					cast_dict['character'] = character
				else:
					cast_dict['character'] = "N/A"
			
			cast_values.append(cast_dict)

		#for tv shows reviews
		review_url="https://api.themoviedb.org/3/tv/"+str(id)+"/reviews?api_key=ef0f49cc4f747effb674303a7c49e03a&lan guage=en-US&page=1"
		show_more_review = requests.get(review_url).content
		review_data = json.loads(show_more_review.decode('utf-8'))
		review_val = review_data['results']
		# review_data = review_data[:5]
		review_values = []
		for review in review_val[:5]:
			reviews_dict = {}
			if 'username' in review['author_details']:
				# username_details = review['author_details']
				username = review['author_details']['username']
				reviews_dict['username'] = username

			if 'content' in review:
				content = review['content']
				reviews_dict['content'] = content
			
			if 'rating' in review['author_details']:
				# rating_details = review['author_details']
				rating = review['author_details']['rating']
				reviews_dict['rating'] = rating

			if 'created_at' in review:
				if review['created_at']:
					created_at_string = review['created_at'].split('T')[0]
					list_created_at=created_at_string.split('-')
					created_at=list_created_at[1]+'/'+list_created_at[2]+'/'+list_created_at[0]
					reviews_dict['created_at'] = created_at
				else:
					reviews_dict['created_at'] = "N/A"

			review_values.append(reviews_dict)


		show_more_array.append(content_dict)
		show_more_array.append(cast_values)
		show_more_array.append(review_values)
		
	return jsonify(show_more_array)


@app.route("/search", methods = ['GET'])
@cross_origin(allow_headers=['Content-Type'])
def search():
	keyword = request.args.get("keyword")
	category = request.args.get("category")
	# print(keyword,category)

	if category == "movies":
		url = "https://api.themoviedb.org/3/search/movie?api_key=ef0f49cc4f747effb674303a7c49e03a&query="+keyword+"&language=en-US&page=1&include_adult=false"
		trending_movies = requests.get(url).content
		data = json.loads(trending_movies.decode('utf-8'))
		values = data['results']
		movie_genres = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=ef0f49cc4f747effb674303a7c49e03a&language=en-US").json()["genres"]
		arr = []
		if values:
			new_values = values[:10]
			for val in new_values:
				movies_dict = {}
				if 'id' in val:
					id = val['id']
					movies_dict['id'] = id

				if 'title' in val:
					title = val['title']
					movies_dict['title'] = title

				if 'overview' in val:
					if val['overview']:
						overview = val['overview']
						movies_dict['overview'] = overview
					else:
						movies_dict['overview'] = "N/A"

				if 'poster_path' in val:
					poster_url = "https://image.tmdb.org/t/p/w500"
					poster_path = val['poster_path']
					if poster_path:
						movies_dict['poster_path'] = poster_url+poster_path
					else:
						movies_dict['poster_path'] = "https://cinemaone.net/images/movie_placeholder.png"

				if 'release_date' in val:
					if val['release_date']:
						release_date_list = val['release_date'].split('-')
						release_date = release_date_list[0]
						movies_dict['release_date'] = release_date
					else:
						movies_dict['release_date'] = "N/A"

				if 'vote_average' in val:
					vote_average = val['vote_average']
					movies_dict['vote_average'] = vote_average
				
				if 'vote_count' in val:
					vote_count = val['vote_count']
					movies_dict['vote_count'] = vote_count

				genre_array=[]
				for genre in movie_genres:
					for gid in val['genre_ids']:
						if gid==genre["id"]:
							genre_array.append(genre["name"])
				genre_array = ', '.join(genre_array)
				if len(genre_array) == 0:
					movies_dict['genre_ids'] = "N/A"
				else:
					movies_dict['genre_ids'] = genre_array
					

				arr.append(movies_dict)

	elif category == "show":
		url = "https://api.themoviedb.org/3/search/tv?api_key=ef0f49cc4f747effb674303a7c49e03a&query="+keyword+"&language=en-US&page=1&include_adult=false"
		trending_show = requests.get(url).content
		show_data = json.loads(trending_show.decode('utf-8'))
		show_values = show_data['results']
		show_genres = requests.get("https://api.themoviedb.org/3/genre/tv/list?api_key=ef0f49cc4f747effb674303a7c49e03a&language=en-US").json()["genres"]

		arr = []
		if show_values:
			new_values = show_values[:10]
			for val in new_values:
				show_dict = {}
				if 'id' in val:
					id = val['id']
					show_dict['id'] = id

				if 'name' in val:
					name = val['name']
					show_dict['name'] = name

				if 'overview' in val:
					if val['overview']:
						overview = val['overview']
						show_dict['overview'] = overview
					else:
						show_dict['overview'] = "N/A"

				if 'poster_path' in val:
					poster_url = "https://image.tmdb.org/t/p/w500"
					poster_path = val['poster_path']
					if poster_path:
						show_dict['poster_path'] = poster_url+poster_path
					else:
						show_dict['poster_path'] = "https://cinemaone.net/images/movie_placeholder.png"

				if 'first_air_date' in val:
					if val['first_air_date']:
						first_air_date_list = val['first_air_date'].split('-')
						first_air_date = first_air_date_list[0]
						show_dict['first_air_date'] = first_air_date
					else: 
						show_dict['first_air_date'] = "N/A"

				if 'vote_average' in val:
					vote_average = val['vote_average']
					show_dict['vote_average'] = vote_average
				
				if 'vote_count' in val:
					vote_count = val['vote_count']
					show_dict['vote_count'] = vote_count

				genre_array=[]

				for genre in show_genres:
					for gid in val['genre_ids']:
						if gid==genre["id"]:
							genre_array.append(genre["name"])
				genre_array = ', '.join(genre_array)
				if len(genre_array) == 0:
					show_dict['genre_ids'] = "N/A"
				else:
					show_dict['genre_ids'] = genre_array

					

				arr.append(show_dict)

	elif category == "both":
		url = "https://api.themoviedb.org/3/search/multi?api_key=ef0f49cc4f747effb674303a7c49e03a&query="+keyword+"&language=en-US&page=1&include_adult=false"
		trending_both = requests.get(url).content
		both_data = json.loads(trending_both.decode('utf-8'))
		both_values = both_data['results']
		movie_genres = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=ef0f49cc4f747effb674303a7c49e03a&language=en-US").json()["genres"]
		show_genres = requests.get("https://api.themoviedb.org/3/genre/tv/list?api_key=ef0f49cc4f747effb674303a7c49e03a&language=en-US").json()["genres"]
		arr = []
		# pprint.pprint(both_values)
		if both_values:
			counter = 0
			for r in both_values:
				if counter > 9:
					break
				else:
					if r['media_type'] == 'person':
						continue
					elif r['media_type'] == 'movie':
						counter += 1
						movies_dict = {}
						if 'id' in r:
							id = r['id']
							movies_dict['id'] = id

						if 'title' in r:
							title = r['title']
							movies_dict['title'] = title

						if 'overview' in r:
							if r['overview']:
								overview = r['overview']
								movies_dict['overview'] = overview
							else:
								movies_dict['overview'] = "N/A"

						if 'poster_path' in r:
							poster_url = "https://image.tmdb.org/t/p/w500"
							poster_path = r['poster_path']
							if poster_path:
								movies_dict['poster_path'] = poster_url+poster_path
							else:
								movies_dict['poster_path'] = "https://cinemaone.net/images/movie_placeholder.png"

						if 'release_date' in r:
							if r['release_date']:
								release_date_list = r['release_date'].split('-')
								release_date = release_date_list[0]
								movies_dict['release_date'] = release_date
							else:
								movies_dict['release_date'] = "N/A"

						if 'vote_average' in r:
							vote_average = r['vote_average']
							movies_dict['vote_average'] = vote_average
						
						if 'vote_count' in r:
							vote_count = r['vote_count']
							movies_dict['vote_count'] = vote_count

						genre_array=[]
						for genre in movie_genres:
							for gid in r['genre_ids']:
								if gid==genre["id"]:
									genre_array.append(genre["name"])
						genre_array = ', '.join(genre_array)
						if len(genre_array) == 0:
							movies_dict['genre_ids'] = "N/A"
						else:
							movies_dict['genre_ids'] = genre_array
						

						if 'media_type' in r:
							media_type = r['media_type']
							movies_dict['media_type'] = media_type

						arr.append(movies_dict)
							
					elif r['media_type'] == 'tv':
						counter += 1
						show_dict = {}
						if 'id' in r:
							id = r['id']
							show_dict['id'] = id

						if 'name' in r:
							name = r['name']
							show_dict['name'] = name

						if 'overview' in r:
							if r['overview']:
								overview = r['overview']
								show_dict['overview'] = overview
							else:
								show_dict['overview'] = "N/A"

						if 'poster_path' in r:
							poster_url = "https://image.tmdb.org/t/p/w500"
							poster_path = r['poster_path']
							if poster_path:
								show_dict['poster_path'] = poster_url+poster_path
							else:
								show_dict['poster_path'] = "https://cinemaone.net/images/movie_placeholder.png"

						if 'first_air_date' in r:
							if r['first_air_date']:
								first_air_date_list = r['first_air_date'].split('-')
								first_air_date = first_air_date_list[0]
								show_dict['first_air_date'] = first_air_date
							else:
								show_dict['first_air_date'] = "N/A"

						if 'vote_average' in r:
							vote_average = r['vote_average']
							show_dict['vote_average'] = vote_average
						
						if 'vote_count' in r:
							vote_count = r['vote_count']
							show_dict['vote_count'] = vote_count

						genre_array=[]
						for genre in show_genres:
							for gid in r['genre_ids']:
								if gid==genre["id"]:
									genre_array.append(genre["name"])
						genre_array = ', '.join(genre_array)
						if len(genre_array) == 0:
							show_dict['genre_ids'] = "N/A"
						else:
							show_dict['genre_ids'] = genre_array
							

						if 'media_type' in r:
							media_type = r['media_type']
							show_dict['media_type'] = media_type

						arr.append(show_dict)
				
	return jsonify(arr)


if __name__ == '__main__':
    app.run()