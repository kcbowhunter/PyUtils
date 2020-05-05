#!/usr/bin/python3

import Jpeg1

import os
import sys
import binascii

#process script arguments
if len(sys.argv) != 2:
    print("Usage: JpegGetAllMarkerData.py file.jpg ")
    print("i.e. : JpegGetMerkerData.py Snow.jpg")
    print("Extract Marker data for each jpeg chunk")
    sys.exit(1)

jpgfile = sys.argv[1]

if not os.path.exists(jpgfile):
    print("Error: Unable to open file: " + jpgfile)
    sys.exit(2)

print("Processing jpg: " + jpgfile)

jpegdata = bytearray()
f = open(jpgfile, "rb")
jpegdata = f.read()
f.close()

print("Read {0} bytes from {1}".format(len(jpegdata), jpgfile))

(markers, offsets, lengths) = Jpeg1.GetJpegMarkers(jpegdata)
print("Markers, offsets etc read from " + jpgfile)

Jpeg1.PrintJpegChunks(jpgfile, markers, offsets, lengths)

# now find the desired marker
count = 0
found = False
mpos = -1
for x in markers:
    mpos = mpos + 1
    m = markers[mpos]
    o = offsets[mpos]
    l = lengths[mpos]

    markername = Jpeg1.GetMarkerName(m)

#    print("Found marker 0x{0:02x} {2:4} ".format(x, markername))

    if l == 0:
        continue

#    print("Marker 0xFF{0:02X} found at offset {1} with length {2} bytes".format(markers[mpos], offsets[mpos], lengths[mpos]))

    data = jpegdata[o:o+l+3]

#    sdata = str(binascii.hexlify(data))
#    sdata = sdata[2:-1]
#    print(data)
#    print(sdata)
#    print("Length of byte str is {0} characters".format(len(sdata)))

    outfile = str(mpos) + "_" + markername + ".bin"
    f = open(outfile, "wb")
    f.write(data)
    f.close()

print("All Done!")
