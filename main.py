import argparse
import math

# the following sets up the arg parse technique
# The commands follow the rubric and implemented optional arguments
# to allow the user to freely choose what order they want to input the info

parser = argparse.ArgumentParser(description='Direct Mapped Cache Simulator')
parser.add_argument('-type', '--cacheType', type=str,metavar='', help='type of cache')
parser.add_argument('-cache_size', '--cacheSize', type=int, metavar='', help='total cache size in bytes')
parser.add_argument('-block_size','--blockSize', type=int, metavar='', help='the size of a block in bytes')
parser.add_argument('-memfile','--txtInput', type=str, metavar='', help='an input text that contains the sequence of memory accesses')
args = parser.parse_args();

#byteOffset and memAddressLen are constant
byteOffset = 2
memAddressLen = 32

#Checks if input is a power of 2. Used for checking cache size and block size input
def isPowerOfTwo(value):
  if value == 0:
    return False

  while (value != 1):
    if (value % 2 != 0):

      return False
    
    value = value // 2

  return True

#Converts binary values to decimal
def binaryToDecimal(binary):
    binary = int(binary)
    decimal, counter = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, counter)
        binary = binary//10
        counter += 1
    return int(decimal)


if __name__ == '__main__':
  #Inputs are acquired from parser
  cacheType = args.cacheType
  cacheSize = args.cacheSize
  blockSize = args.blockSize
  txtInput = args.txtInput

  #Checks if the inputs are a power of 2 and if the cache size does not exceed 256,the block size does not exceed 64, and whether the cacheType input is correct 
  if (isPowerOfTwo(cacheSize) and isPowerOfTwo(blockSize) and cacheSize <= 256 and blockSize <= 64 and cacheType == 'd'):
    memAddressList, memAddressBin, tagList, indexList, hitCheckList, hitList, output = [], [], [], [], [], [], []
    flag = False
    
    #The list of commands is meant for debugging
    #print("cacheType: ",args.cacheType)
    #print("cacheSize: ",args.cacheSize)
    #print("blockSize: ",args.blockSize)
    #print("txtInput: ", args.txtInput)

    #The number of words is calculated by dividing the size of the block by 4 and the logarithm is taken in order to find the bit offset value
    numOfWords = blockSize/4
    wordOffset = int(math.log2(numOfWords))

    numOfBlocks = cacheSize/blockSize
    indexOffset = int(math.log2(numOfBlocks))

    #number of bits for tag is calculated by subtracting the offsets from the total number of bits of the memory address 
    tagBits = memAddressLen - indexOffset - wordOffset - byteOffset
    #memory address values are acquired from file
    with open(txtInput) as NumFile:

      [memAddressList.append(line.strip("\n")) for line in NumFile.readlines()]

    #memory addresses are converted to binary values
    for memAddress in memAddressList:

      memAddressBin.append(str(bin(int(memAddress, 16)))[2:].zfill(memAddressLen))

    #list of tag values and list of index values are stored
    for binVal in memAddressBin:
      tag = binVal[0:tagBits]
      index = binVal[tagBits: tagBits+indexOffset]
      tagList.append(tag)
      indexList.append(index)

    #Using the information of tag and index, the double loop checks whether a hit or miss is found
    #If there is a miss, the address, tag and index are stored in a list and when the next memory address is accessed, it will check that list. The list is called hitCheckList
    #If the address' tag and index values are in the hitCheckList, it is a hit
    #Unaligned memory address are evaluatd by checking whether the decimal values of the memory addresses are divisible by 4 
    for i in range(0,len(indexList)):
      if binaryToDecimal(binaryToDecimal(memAddressBin[i]) % 4 == 0):
        tagIndexCheck = [tagList[i],indexList[i]]
        if tagIndexCheck not in hitCheckList:
          hitList.append("MISS")
          for check in hitCheckList:
            if check[1] ==tagIndexCheck[1]:
              check[0] = tagIndexCheck[0]
              flag = True
          if not flag:
            hitCheckList.append(tagIndexCheck)
        else:
          hitList.append("HIT")
          numOfHits = 0
      else:
        hitList.append("UNALIGNED")
    
    #Hit Rate is calculated
    for check in hitList:

      if check == "HIT":
        numOfHits += 1
    
    hitRate = numOfHits/len(hitList)
    hitRate = "Hit rate is: " + str(hitRate*100) + '%'
    
    #print(hitList)
    #The code below shows the correct output
    for i in range(0,len(hitList)):
      output.append(str(memAddressList[i])+"|"+str(tagList[i])+"|"+str(indexList[i])+"|"+hitList[i])
    #print(output)
    with open('output.txt', 'w') as f:
      for i in range(0,len(hitList)):
        f.write(output[i]+"\n")
        #f.write('/n')
      f.write(hitRate)
    #The following is for debugging
    #print(tagIndex)
    #print("tagBits: ", tagBits)
    #print("indexOffset: ", indexOffset)
    #print("wordOffset: ", wordOffset)
    #print("byteOffset: ", byteOffset)

    
  #The info below notifies the user what is wrong with their input
  else:
    print("Error in input")
