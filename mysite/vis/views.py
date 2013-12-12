from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
import json
from models import Torrent
from models import TorrentDatetime
from models import TorrentLocation
import MySQLdb as mdb
import MySQLdb.cursors as cursors
from django.http import HttpResponse

host = 'tal.xvm.mit.edu'
user = 'neo'
password = '1234'
db = '6885'

def index(request):
	return render_to_response('vis/index.html', locals(), context_instance = RequestContext(request))

def get_torrents(request):
	data = json.dumps(get_torrents_from_db())
	return HttpResponse(data, content_type="application/json")

def get_locations(request):
	data = json.dumps(generate_just_locations())
	return HttpResponse(data, content_type="application/json")

def get_filtered_torrents(request, lb, books, music, movies, tv, pirate, kat, seedpeer):
	if lb < 10:
		data = generate_torrents(0, 10, books, music, movies, tv, pirate, kat, seedpeer)
	else:
		data = generate_torrents(int(lb), int(lb)+10, books, music, movies, tv, pirate, kat, seedpeer)
	return HttpResponse(data, content_type="application/json")

def get_titled_torrents(request, lb, books, music, movies, tv, pirate, kat, seedpeer, title):
	if lb < 10:
		data = generate_torrents_with_title(0, 10, books, music, movies, tv, pirate, kat, seedpeer, title)
	else:
		data = generate_torrents_with_title(int(lb), int(lb)+10, books, music, movies, tv, pirate, kat, seedpeer, title)
	return HttpResponse(data, content_type="application/json")

def get_torrents_from_db():
	cursor = db_connection(host, user, password, db)
	torrents = get_first_torrents_from_cursor(cursor)
	return compile_torrent_list(torrents)

def generate_just_locations():
	cursor = db_connection(host, user, password, db)
	location_iter = get_all_locations_from_cursor(cursor)
	return get_locations_from_db(location_iter)

def get_locations_from_db(location_iter):
	t_list = []
	for loc in location_iter:
		t_dict = {}
		t_dict['lat'] = loc[0]
		t_dict['lon'] = loc[1]
		t_dict['value'] = .000001
		t_list.append(t_dict)
	total = {}
	total['max'] = 10000
	total['data'] = t_list
	return total

def compile_torrent_list(torrents):
	t_list = []
	for t in torrents:
		t_dict = {}
		t_dict['t_id'] = t[0]
		t_dict['t_website'] = t[1]
		t_dict['t_category'] = t[2]
		t_dict['t_title'] = t[3]
		t_dict['t_url'] = t[4]
		t_dict['t_size'] = t[5]
		t_dict['t_sizeType'] = t[6]
		# t_dict['t_seeders'] = t[7]
		# t_dict['t_leechers'] = t[8]
		t_list.append(t_dict)
	return t_list

def generate_torrents(lb, ub, books, music, movies, tv, pirate, kat, seedpeer):
	(st1, st2) = generate_category_strings(books, music, movies, tv)
	loc_query_str = ''
	torrent_query_str = ''
	(web_st1, web_st2, web_st3) = generate_website_strings(pirate, seedpeer, kat)

	loc_query_str = "SELECT latitude, longitude from torrent_location, torrent "+\
	"WHERE torrent.id = torrent_id AND (t_category like "+"'%"+st1+"%'"+" OR t_category like "+"'%"+st2+"%'"+") "+\
	"AND (t_website like "+"'%"+web_st1+"%'"+" OR t_website like "+"'%"+web_st2+"%'"+" OR t_website like "+"'%"+web_st3+"%'"+") "+\
	"LIMIT 100000" 

	# torrent_query_str = "select torrent.id, t_website, t_category, t_title, t_url, t_size, t_sizeType, seeders, leechers "+\
	# "from torrent, torrent_datetime "+\
	# "where torrent.id = torrent_datetime.torrent_id "+\
	# "and (t_category like "+"'%"+st1+"%'"+" or t_category like "+"'%"+st2+"%') "+\
	# "and (t_website like "+"'%"+web_st1+"%'"+" or t_website like "+"'%"+web_st2+"%'"+" or t_website like "+"'%"+web_st3+"%'"+") "+\
	# "limit 10 offset "+str(lb)

	torrent_query_str = "select id, t_website, t_category, t_title, t_url, t_size, t_sizeType "+\
	"from torrent "+\
	"where (t_category like "+"'%"+st1+"%'"+" or t_category like "+"'%"+st2+"%') "+\
	"and (t_website like "+"'%"+web_st1+"%'"+" or t_website like "+"'%"+web_st2+"%'"+" or t_website like "+"'%"+web_st3+"%'"+") "+\
	"limit 10 offset "+str(lb)

	print torrent_query_str
	print loc_query_str

	cursor = db_connection(host, user, password, db)

	location_iter = get_query_from_cursor(cursor, loc_query_str)
	torrent_iter = get_query_from_cursor(cursor, torrent_query_str)

	locations = get_locations_from_db(location_iter)
	torrents = compile_torrent_list(torrent_iter)

	t_dict = {}
	t_dict['locations'] = locations
	t_dict['torrents'] = torrents
	# print t_dict
	return json.dumps(t_dict)

def generate_torrents_with_title(lb, ub, books, music, movies, tv, pirate, kat, seedpeer, title):
	(st1, st2) = generate_category_strings(books, music, movies, tv)
	loc_query_str = ''
	torrent_query_str = ''
	(web_st1, web_st2, web_st3) = generate_website_strings(pirate, seedpeer, kat)

	loc_query_str = "SELECT latitude, longitude from torrent_location, torrent "+\
	"WHERE torrent.id = torrent_id AND (t_category like "+"'%"+st1+"%'"+" OR t_category like "+"'%"+st2+"%'"+") "+\
	"AND (t_website like "+"'%"+web_st1+"%'"+" OR t_website like "+"'%"+web_st2+"%'"+" OR t_website like "+"'%"+web_st3+"%'"+") "+\
	"AND (t_title like "+"'%"+title+"%' "+\
	"OR t_title like "+"'%"+title.lower()+"%') "+\
	"LIMIT 100000" 

	# torrent_query_str = "select torrent.id, t_website, t_category, t_title, t_url, t_size, t_sizeType, seeders, leechers "+\
	# "from torrent, torrent_datetime "+\
	# "where torrent.id = torrent_datetime.torrent_id "+\
	# "and (t_category like "+"'%"+st1+"%'"+" or t_category like "+"'%"+st2+"%') "+\
	# "and (t_website like "+"'%"+web_st1+"%'"+" or t_website like "+"'%"+web_st2+"%'"+" or t_website like "+"'%"+web_st3+"%'"+") "+\
	# "and (t_title like "+"'%"+title+"%' "+\
	# "or t_title like "+"'%"+title.lower()+"%') "+\
	# "limit 10 offset "+str(lb)

	torrent_query_str = "select id, t_website, t_category, t_title, t_url, t_size, t_sizeType "+\
	"from torrent "+\
	"where (t_category like "+"'%"+st1+"%'"+" or t_category like "+"'%"+st2+"%') "+\
	"and (t_website like "+"'%"+web_st1+"%'"+" or t_website like "+"'%"+web_st2+"%'"+" or t_website like "+"'%"+web_st3+"%'"+") "+\
	"and (t_title like "+"'%"+title+"%' "+\
	"or t_title like "+"'%"+title.lower()+"%') "+\
	"limit 10 offset "+str(lb)

	print torrent_query_str
	print loc_query_str

	cursor = db_connection(host, user, password, db)
	
	location_iter = get_query_from_cursor(cursor, loc_query_str)
	torrent_iter = get_query_from_cursor(cursor, torrent_query_str)

	locations = get_locations_from_db(location_iter)
	torrents = compile_torrent_list(torrent_iter)

	t_dict = {}
	t_dict['locations'] = locations
	t_dict['torrents'] = torrents
	# print t_dict
	return json.dumps(t_dict)

def generate_category_strings(books, music, movies, tv):
	st1 = ''
	st2 = ''
	if books == 't':
		st1 = 'books'
		st2 = 'books'
	elif music=='t':
		st1 = 'music'
		st2 = 'Music'
	elif movies == 't':
		st1 = 'movies'
		st2 = 'Movies'
	elif tv == 't':
		st1 = 'tv'
		st2 = 'TV Shows'
	else:
		st1 = ''
		st2 = ''
	return (st1, st2)

def generate_website_strings(pirate, seedpeer, kat):
	st1 = 'junk'
	st2 = 'junk'
	st3 = 'junk'
	if pirate == 't':
		st1 = 'thepiratebay'
	if seedpeer=='t':
		st2 = 'seedpeer'
	if kat == 't':
		st3 = 'kat'
	if pirate == 'f' and seedpeer == 'f' and kat == 'f':
		st1 = ''
		st2 = ''
		st3 = ''
	return (st1, st2, st3)

def db_connection(host, user, password, db):
	connection = mdb.connect(host=host, user=user, passwd=password, db=db, cursorclass=cursors.SSCursor)
	return connection.cursor()

def get_all_locations_from_cursor(cursor):
	query = "SELECT latitude, longitude FROM torrent_location LIMIT 100000"
	try:
		cursor.execute(query)
		for row in cursor:
			yield row

	except Exception as e:
		print "Error when executing query", e

def get_first_torrents_from_cursor(cursor):
	query = "select torrent.id, t_website, t_category, t_title, t_url, t_size, t_sizeType, seeders, leechers "+\
		"from torrent, torrent_datetime "+\
		"limit 10"
	try:
		cursor.execute(query)
		for row in cursor:
			yield row

	except Exception as e:
		print "Error when executing query", e

def get_query_from_cursor(cursor, query):
	try:
		cursor.execute(query)
		for row in cursor:
			yield row

	except Exception as e:
		print "Error when executing query", e
