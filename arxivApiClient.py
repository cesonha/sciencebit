import urllib
import sys
import xml.dom.minidom
from xml.dom.minidom import parse
import json
from json import JSONEncoder as encoder

def getPaperList(terms, n):
	query = terms
	url = "http://export.arxiv.org/api/query?search_query=abs:\"" + query + "\"&sortBy=lastUpdatedDate&sortOrder=descending&max_results=" + str(n)
	data = urllib.urlopen(url).read()
	return data

def retrievePaperInfo(terms): ## terms has to be a list
	outputJson = []
	for term in terms:
		x = getPaperList(term, 3)
		tree = xml.dom.minidom.parseString(x)
		doc = tree.documentElement
		entries = doc.getElementsByTagName("entry")
		jsonEntries = []
		for entry in entries:
			properties = ["title", "id", "published", "summary"]
			x = [(y, entry.getElementsByTagName(y)[0].firstChild.nodeValue) for y in properties]
			author = entry.getElementsByTagName("author")[0]
			author = author.getElementsByTagName("name")[0].firstChild.nodeValue
			x.append(("author", author))
			score = 0
			abstract = entry.getElementsByTagName("summary")[0].firstChild.nodeValue 
			# if (term in abstract): score += 1
			x.append(("score", str(int(100 * score / float(len(terms))))))
			jsonEntries.append(x)

		for entry in jsonEntries:
			jsonEntry = {}
			jsonEntry["entry"] = {}
			for field in entry:
				jsonEntry["entry"][field[0]] = field[1]
			categories = []
			for term in terms:
				if (term in jsonEntry["entry"]["summary"]):
					categories.append(term)
			jsonEntry["entry"]["categories"] = categories
			outputJson.append(jsonEntry)
	return encoder().encode(outputJson)

retrievePaperInfo(["Graph Theory"])


