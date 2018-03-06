#!/usr/bin/env python

####File parameter
#----------------------------------------------------------------
inputfile = "no file"
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, nargs='?', help="specifies the inputfile. Must be .txt", default=inputfile, action="store")
args = parser.parse_args()
inputfile = args.file
print("Inputfile:",inputfile)

import snap
G1 = snap.LoadEdgeList(snap.PNGraph, inputfile, 0, 1)
for NI in G1.Nodes():
	if NI.GetOutDeg() == 0:
		print NI.GetId()