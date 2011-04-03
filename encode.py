#!/usr/bin/python
#!encoding=utf8
import Image
import sys

__bitmasks_sparse = [1,2,4,8,16,32,64,128]
__bitmasks_dense = []
for i in __bitmasks_sparse:
  __bitmasks_dense.append(255-i)

def __embed(data, band, row):
  for (i, byte) in enumerate(data):
    for j in range(0,8):
      if byte&__bitmasks_sparse[j] > 0: # bitinn er 1
        band[8*i+j,row] = __bitmasks_sparse[0] | band[8*i+j,0]
      else: # bitinn er 0
        band[8*i+j,row] = __bitmasks_dense[0] & band[8*i+j,0]

def encode(data, im):
  # Check whether the image is large enough.
  if im.size[0] < 32:
    print "Image should be at least 32 pixels wide."
    return None

  datasize = len(data)
  imsize = im.size[0]*(im.size[1]-1)

  if imsize < datasize*8: # ÞETTA ER EKKI NÓG!
    print "Image is not large enough."
    return None
  
  # Actual work.
  bands = im.split()
  blue = bands[2].load()

  # First line of pixels contains the size of the data in the first 32 pixels.
  width = im.size[0]
  bytes_per_row = width/8
  wholerows = datasize/bytes_per_row
  lastrow = datasize%bytes_per_row

  a = [wholerows&255, (wholerows/256)&255, lastrow&255, (lastrow/256)&255]
  
  __embed(a, blue, 0)

  for i in range(wholerows):
    __embed(data[i*bytes_per_row:(i+1)*bytes_per_row], blue, i+1)

  __embed(data[wholerows*bytes_per_row:wholerows*bytes_per_row+lastrow], \
      blue, wholerows+1)

  return Image.merge(im.mode, bands)

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print "Invalid number of arguments. Should be 3."
  else:
    data_name = sys.argv[1]
    in_name = sys.argv[2]
    out_name = sys.argv[3]

    data_str = open(data_name, 'rb').read()
    data_bytes = map(lambda x:ord(x), data_str)
    try:
      image = Image.open(in_name)
    except Exception as e:
      print e
      sys.exit(1)

    result = encode(data_bytes, image)

    result.save(out_name)
