#!/usr/bin/python

import traceback, datetime
from credentials import *
from pinboardHelper import *
from diffbotHelper import *
from sanitize import *
from evernoteHelper import *

def main():
	try:
		try:
			f = open ("lastUpdate.txt", "r")
			fromdt = f.read().strip()
			f.close()
			bookmarkList = getBookmarksFromDate(PinboardAPIToken, fromdt)
		except IOError:
			# If lastUpdate.txt doesn't exist.
			# It means that the program is being run for the first time.
			# So get all bookmarks.
			bookmarkList = getAllBookmarks(PinboardAPIToken)

		# We have fetched bookmarks uptill now.
		todt = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
	except:
		print "Fetching bookmarks from Pinboard failed."
		traceback.print_exc()
		print
		exit(1)

	notesCreated = 0
	failedURLs = open("failedURLs.txt", "a")
	for bookmark in bookmarkList:

		try:
			html = extractArticle(DiffbotToken, bookmark[0], html=True)
		except:
			print "Extracting article using Diffbot failed."
			print bookmark[0]
			failedURLs.write(bookmark[0] + "\n")
			traceback.print_exc()
			print
			continue
			#exit(1)

		try:
			enml = sanitize(html)
		except:
			print "Converting article from HTML to ENML failed."
			print bookmark[0]
			failedURLs.write(bookmark[0] + "\n")
			traceback.print_exc()
			print
			continue
			#exit(1)

		try:
			sendToEvernote(bookmark[1], bookmark[0], enml, EvernoteDeveloperToken)
		except:
			print "Storing note in Evernote failed."
			print bookmark[0]
			failedURLs.write(bookmark[0] + "\n")
			print enml
			print
			traceback.print_exc()
			print
			continue
			#exit(1)

		notesCreated += 1

	failedURLs.close()

	# Update the lastUpdate time.
	f = open("lastUpdate.txt", "w")
	f.write(todt)
	f.close()

	print "Total number of notes created = " + str(notesCreated)


if __name__ == "__main__":
	main()
