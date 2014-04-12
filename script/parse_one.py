#!/usr/bin/python

import argparse
import json
import os
from os import path

def flatten(l):
	return [item for sublist in l for item in sublist]

def main():
	parser = argparse.ArgumentParser(
		description='generate a cohesive vote record')
	parser.add_argument('congress', type=str,
			help='directory that contains congressional vote record and bills')
	parser.add_argument('output', type=str,
			help='file to output json')
	args = parser.parse_args()

	out = open(args.output, 'w')

	vbp = path.join(args.congress, 'votes')
	votes_dirs = [path.join(vbp, y) for y in os.listdir(vbp)
			if y[0] != '.']
	votes = []
	for y in votes_dirs:
		votes += [path.join(y, d, 'data.json') for d in os.listdir(y)
				if d[0] != '.']
	parsed = [parse_vote(f) for f in votes]
	bbp = path.join(args.congress, 'bills')
	res = {'bills': [get_vote_extras(p, bbp) for p in parsed if not p is None]}
	json.dump(res, out)
	out.close()

def get_vote_extras(b, bbp):
	p = path.join(bbp, b["type"], b["type"] + str(b["number"]), 'data.json')
	try:
		with open(p) as f:
			rec = json.load(f)
	except IOError:
		print "no such file:", p, "from", b["_srcfile"] 
		return
	sponsor = rec["sponsor"]
	if sponsor is None:
		print "warning: null sponsor in", p
		del b["votes"]["_"]
		return b
	spnsr = {
			"state": sponsor["state"],
			"district": sponsor["district"],
			"thomas_id": sponsor["thomas_id"],
			"name": sponsor["name"]
	}
	b["sponsor"] = spnsr
	v = b["votes"]["_"]
	if search_votes(spnsr, v[0]):
		spnsr["vote"] = "yay"
	elif search_votes(spnsr, v[1]):
		spnsr["vote"] = "nay"
	elif search_votes(spnsr, v[2]):
		spnsr["vote"] = "present"
	elif search_votes(spnsr, v[3]):
		spnsr["vote"] = "not present"
	else:
		spnsr["vote"] = None
		print "warning: couldn't find sponsor in voting record from", b["_srcfile"]
	del b["votes"]["_"]
	return b

def search_votes(s, vs):
	for v in vs:
		if v == "VP":
			continue
		if v["state"] == s["state"]:
			dn = v["display_name"]
			n = s["name"]
			if dn.split(" ")[0] == n.split(", ")[0]:
				# match!
				# copy data over
				s["id"] = v["id"]
				s["party"] = v["party"]
				return True
	return False

def parse_vote(p):
	with open(p) as f:
		rec = json.load(f)
	category = rec["category"]
	if category != 'passage':
		return None
	if rec["type"] != 'On Passage of the Bill':
		return None
	rresult = rec["result"]
	if rresult == 'Bill Passed' or rresult == 'Passed':
		passed = True
	elif rresult == 'Failed' or rresult == 'Bill Defeated':
		passed = False
	else:
		print "warning: invalid value for passage:", passed
		passed = None

	if not "bill" in rec:
		if "treaty" in rec:
			# treaty not bill
			return None
		print "warning: record claims to be bill but does not have bill object"
		print "         from:", p
		return None

	bill = {
			"passed": passed,
			"congress": rec["bill"]["congress"],
			"type": rec["bill"]["type"],
			"number": rec["bill"]["number"],
			"title": rec["bill"].get("title"),
			"year": rec["date"][:4],
			"date": rec["date"],
			"chamber_number": rec["number"],
			"_srcfile": p
	}

	# get votes by party
	votes = rec["votes"]
	keys = votes.keys()
	if 'Yay' in keys:
		yays = votes["Yay"]
		nays = votes["Nay"]
	elif 'Yea' in keys:
		yays = votes["Yea"]
		nays = votes["Nay"]
	elif 'Aye' in keys:
		yays = votes["Aye"]
		nays = votes["No"]
	else:
		print keys
		print bill
		print "Couldn't find Yay vote"
		return None
	present = votes["Present"]
	not_voting = votes["Not Voting"]
	def make_count(seg):
		c = {}
		for v in seg:
			if v == "VP":
				# TODO how do we do this
				print "warning: ignoring VP vote"
				continue
			p = v["party"]
			if p in c:
				c[p] += 1
			else:
				c[p] = 1
		return c
	bill["votes"] = {
		"yay": make_count(yays),
		"nay": make_count(nays),
		"present": make_count(present),
		"not_voting": make_count(not_voting),
		"_": [yays, nays, present, not_voting] # removed by get_extras
			}

	return bill

if __name__ == '__main__':
	main()
