#!/usr/bin/python3

import Jpeg1
import sys


if len(sys.argv) != 2:
    print("Usage: JpegGetComments filename")
    sys.exit(1)

filename = sys.argv[1]

Jpeg1.CheckIfFileExists(filename)

data = Jpeg1.ReadBinaryFile(filename)

(markers, offsets, lengths) = Jpeg1.GetJpegMarkers(data)

comcount = 0
count = -1
for x in markers:
    count += 1
    if x == 0xfe:
        o = offsets[count]
        l = lengths[count]
        print("Found COM marker at offset {0} with length {1}".format(o, l))
        filename = "com" + str(comcount)
        f = open(filename, "wb")
        f.write(data[o+4:o+4+l-2])
        f.close()
        comcount = comcount + 1

print("All Done!")