#!/usr/bin/python
#!encoding=utf8
import Image
import sys

__bitmasks_sparse = [1,2,4,8,16,32,64,128]

def __debed(band, row, amount):
  data = []
  for i in range(0, amount):
    currentbyte = 0
    for j in range(0,8):
      if band[8*i+j,row]&__bitmasks_sparse[0] > 0: #bitinn er 1
        currentbyte = currentbyte + __bitmasks_sparse[j]
      else: # bitinn er 0
        pass
    data.append(currentbyte)

  return data

def decode(im):
  blue = im.split()[2].load()

  info = __debed(blue, 0, 4)
  wholerows = info[0] + info[1]*256
  lastrow = info[2] + info[3]*256

  width = im.size[0]
  bytes_per_row = width/8

  data = []
  for i in range(wholerows):
    data += __debed(blue, i+1, bytes_per_row)

  data += __debed(blue, wholerows+1, lastrow)

  return data

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "Invalid number of arguments. Should be 2."
  else:
    im_name = sys.argv[1]
    data_name = sys.argv[2]

    image = Image.open(im_name)

    result_raw = decode(image)
    result_chr = map(lambda x:chr(x), result_raw)
    
    data = open(data_name,'wb')
    for c in result_chr:
      data.write(c)
    data.close()
