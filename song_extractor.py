# export HAR file of gaana.com website from developer 
# options in chrome which will include all the data received
# from gaana.com server to your browser
# 
# Dependencies : VLC
#
# python3 gaana_song_extractor.py <HAR file path> [gaana|wynk]>
# 
import json, requests, re, os, sys
import subprocess, shutil
from urllib import parse

temp1 = 'temp1/'
temp2 = 'temp2/'
outdir = 'converted_mp3_songs/'

GAANA 	= 'gaana'
WYNK 	= 'wynk'
SPOTIFY	= 'spotify'

if len(sys.argv) < 3:
	print(f"python3 gaana_song_extractor.py <HAR file path> <{GAANA}|{WYNK}|{SPOTIFY}>")
	exit()

harfilepath = sys.argv[1]

plateform = sys.argv[2]
if plateform not in [GAANA, WYNK, SPOTIFY]:
	print("invalid plateform as last argument")
	exit()

# if temp directories exists then abort 
if os.path.exists(temp1) or os.path.exists(temp2):
	print("temp1 and temp2 folders exists")
	exit()

# create temp folders
os.mkdir(temp1)
os.mkdir(temp2)

if not os.path.exists(outdir):
	os.mkdir(outdir)

def getfilename(path):
	if plateform == GAANA:
		return path.split("/")[-2]
	elif plateform == WYNK:
		return "_".join(path.split("/")[1:3])+path.split("/")[-2]
	elif plateform == SPOTIFY:
		return path.split('/')[-1]
	else:
		return path.split("/")[-2]


try:
	with open(harfilepath, 'r') as harfile:
		har = json.load(harfile)

	entries = har['log']['entries']

	for i in range(len(entries)):
		url = entries[i]['request']['url']
		path = parse.urlsplit(url).path

		is_valid_path = False

		# print(path)
		if plateform == SPOTIFY:
			is_valid_path = path[:7] == '/audio/'
		else:
			is_valid_path = (re.search('\.ts$', path) is not None)


		if is_valid_path:
			# print(i, path)
			filename = getfilename(path)
			with open(temp1+filename, 'a') as file:
				try:
					file.write(entries[i]['response']['content']['text'])
				except Exception as e:
					print(e)

		else:
			pass


	# convert text file into MPEG-2 file format
	for tempfile in os.listdir(temp1):
		with open(temp2+tempfile, 'wb') as out:
			subprocess.call(['base64', '-d', temp1+tempfile], stdout=out)

	# now convert into mp3 format
	# https://superuser.com/questions/388511/how-can-i-make-the-following-conversion-in-vlc-from-the-commandline/390240
	print('converting to mp3 format...')
	for tempfile in os.listdir(temp2):
		os.system('vlc -I dummy "'+temp2+tempfile+'" ":sout=#transcode{acodec=mpga,ab=128}:std{dst="'+outdir+tempfile+'.mp3",access=file}" vlc://quit')

except Exception as e:
	print(e.message)

finally:
	# delete temporary files
	if os.path.exists(temp1):
		shutil.rmtree(temp1)

	if os.path.exists(temp2):
		shutil.rmtree(temp2)
