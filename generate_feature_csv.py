import sys
import csv
import json
import math

dict_month_to_int = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

def is_valid_JSONobject(anyline):
	if 'created_at' in anyline :
		if anyline['lang'] == 'und' :
			return False
		return True
	return False

def isINT_object_retweet(anyline):
	if 'created_at' not in anyline :
		return None
	if anyline['is_quote_status'] == True :
		return 1
	return 0

def get_profile_id(anyline):
	if 'user' not in anyline :
		return -1
	return str(anyline['user']['id'])

def get_profile_followers_count(anyline):
	if 'user' not in anyline:
		return -1
	return anyline['user']['followers_count']


def get_profile_following_count(anyline):
	if 'user' not in anyline:
		return -1
	return anyline['user']['friends_count']

def get_formatted_tweet_date(anyline):
	if 'created_at' not in anyline :
		return None
	date_txt = anyline['created_at']
	date_arr = date_txt.split()
	new_date = str(dict_month_to_int[date_arr[1]]) + '/' + str(int(date_arr[2])) + '/' + date_arr[5]
	return new_date

def get_JSONobject_content(anyline):
	if 'created_at' not in anyline :
		return None
	return anyline['text']

def get_JSONobject_tweet_language(anyline) :
	if 'created_at' not in anyline :
		return None
	return anyline['lang']



def write_feature_into_csv(line_cnt, json_filename, csv_handle):

	file = open(json_filename, 'r')
	#csvfile = open(csv_filename, 'w')
	fd = csv.writer(csv_handle, delimiter=',') #, quoting=csv.QUOTE_NONNUMERIC)

	fd.writerow([
		'author_id',
		'content',
		'language_code',
		'publish_date',
		'following',
		'followers',
		'retweet'
		])

	for line in file :

		row = json.loads(line)

		if not is_valid_JSONobject(row) :
			continue

		_id = get_profile_id(row)
		_date = get_formatted_tweet_date(row)
		_lang = get_JSONobject_tweet_language(row)
		_content = get_JSONobject_content(row)
		_followers_cnt = get_profile_followers_count(row)
		_following_cnt = get_profile_following_count(row)
		_is_retweet = isINT_object_retweet(row)

		fd.writerow([_id, _content, _lang, _date, _following_cnt, _followers_cnt, _is_retweet])

		line_cnt = line_cnt + 1
		print(line_cnt)

	return line_cnt


if __name__ == '__main__' :

	file_list = ['day30.json']
	csv_filename = 'nov30.csv'

	csv_handle = open(csv_filename, 'w')

	line_cnt = 0

	for fname in file_list :
		line_cnt = write_feature_into_csv(line_cnt, fname, csv_handle)
		#print(line_cnt)