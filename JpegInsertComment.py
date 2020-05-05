#!/usr/bin/python3

import sys
import Jpeg1

if len(sys.argv) != 4:
    print("Usage: JpegInsertComment.py source.jpg target.jpg commentfile")
    sys.exit(1)

basefilename = sys.argv[1]
outfilename  = sys.argv[2]
comfilename  = sys.argv[3]

# check if the files exist, exit if not found
Jpeg1.CheckIfFileExists(basefilename)
Jpeg1.CheckIfFileExists(comfilename)

basedata = Jpeg1.ReadBinaryFile(basefilename)
comment  = Jpeg1.ReadBinaryFile(comfilename)

(markers, offsets, lengths) = Jpeg1.GetJpegMarkers(basedata)
print("Markers, offsets etc read from " + basefilename)

Jpeg1.PrintJpegChunks(basefilename, markers, offsets, lengths)

#offset tot he point after the first two chunks
off = offsets[2]

#open the output file
f = open(outfilename, "wb")
f.write(basedata[:off])

temp = bytearray()
temp.append(0xff)
temp.append(0xfe)
print("Comment Length is {0} 0x{0:02x} bytes".format(len(comment)))

# add 2 because as per jpeg/jfif spec, the length includes the two bytes for the length itself
x = len(comment) + 2
if x <= 0xff:
    temp.append(0x00)
    temp.append(x)
else:
    temp.append(x)
f.write(temp)
f.write(comment)

f.write(basedata[off:])

f.close()


print("All Done!")

