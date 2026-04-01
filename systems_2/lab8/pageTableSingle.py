# standard virtual memory page table implementation

# This is a basic implementation of a page table
#   with aging as the replacement policy
# It includes no TLB, multilevel or inverted tables
# It works for only a single process

# The format of a page table entry is:
#   ---Mbit Rbit Pbit frame#

import math

# This is a helper class that decodes any page table entry given to it
#   so we don't have to have all the bit manipulation in the main code
# Note that since we can't pass integers by reference in Python that
#   we use a modify and return pattern for the functions that modify
class PageTableDecoder:
    def __init__(self, frameBits):
        self.frameBits = frameBits

    def getModified(self, pageTableEntry):
        return (pageTableEntry >> (self.frameBits+2)) & 1
    
    def getReferenced(self, pageTableEntry):
        return (pageTableEntry >> (self.frameBits+1)) & 1
    
    def getPresent(self, pageTableEntry):
        return (pageTableEntry >> self.frameBits) & 1
    
    def setModified(self, pageTableEntry):
        return pageTableEntry | (1 << (self.frameBits+2))
    
    def setReferenced(self, pageTableEntry):
        return pageTableEntry | (1 << (self.frameBits+1))
    
    def setPresent(self, pageTableEntry):
        return pageTableEntry | (1 << self.frameBits)
    
    def clearModified(self, pageTableEntry):
        return pageTableEntry & ~(1 << (self.frameBits+2))
    
    def clearReferenced(self, pageTableEntry):
        return pageTableEntry & ~(1 << (self.frameBits+1))
    
    def clearPresent(self, pageTableEntry):
        return pageTableEntry & ~(1 << self.frameBits)
    
    def getFrameNum(self, pageTableEntry):
        return pageTableEntry & ((1 << self.frameBits) - 1)
    
    def replaceFrameNum(self, pageTableEntry, frameNum):
        # First clear the frame number bits
        temp = pageTableEntry & ~((1 << self.frameBits) - 1)
        # Then add in the new frame number
        return temp | frameNum


def displayPageTable(pageTable, decoder, agingR):

    print("Page Table (with associated aging status):")
    print("page#\tmod\tref\tpresent\tframe#\taging\n")
    for i in range(len(pageTable)):
        pageTableEntry = pageTable[i]

        m = decoder.getModified(pageTableEntry)
        r = decoder.getReferenced(pageTableEntry)
        p = decoder.getPresent(pageTableEntry)
        pf = decoder.getFrameNum(pageTableEntry)
 
        print(i, ":\t", m, "\t", r, "\t", p, "\t", pf, "\t", (agingR[i]))
  
def readFile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    # First line is the number of bits for things
    #  Virtual Address, Physical Address, Page Size
    virBits = int(lines[0].split()[0])
    phyBits = int(lines[0].split()[1])
    pageBits = int(lines[0].split()[2])

    # Second line is the number of processes - assumed 1 for this and ignored
    numProcesses = int(lines[1])
    
    # Remove the first two lines
    lines = lines[2:]

    return virBits, phyBits, pageBits, lines

def main():
    virBits, phyBits, pageBits, memAccesses = readFile("testCases/inputOne.txt")

    # Calculate sizes based on the number of bits
    virMemSize = 2 ** virBits

    phyMemSize = 2 ** phyBits
    pageSize = 2 ** pageBits

    print("INITIAL PAGETABLE SETUP:")
    print("  Virtual Mememory Size: ", virMemSize)
    print("  Physical Memory Size: ", phyMemSize)
    print("  Page Size: ", pageSize)

    # Assume 1 process for now

    # Compute values based on the info above
    # These should all be powers of 2 so the divides will be even
    numFrames = phyMemSize // pageSize
    numPages = virMemSize // pageSize
    frameBits = int(math.log2(numFrames))

    # Create the helper to decodee the page table entries
    decoder = PageTableDecoder(frameBits)

    print("  Number of Pages: ", numPages)
    print("  Number of Frames: ", numFrames)
    print("  FrameBits: ", frameBits)

    # Setup physical memory - we won't be inserting/erasing
    #  so arrays work just fine
  
    # Create a free frames list and put all of the frames on it
    freeFrames = [i for i in range(numFrames)]
    print("Free Frames: ", freeFrames)

    # The pageTable should store indices into the pageFrames
    # But also the other needed bits
    # The format is: MRPframe#
    # where frame is the frame number bits
    #  M is modified, R is reference and P is present (all 1 bit)
    # We have a helper class to help decode this information
    pageTable = [0] * numPages
    print("Page Table: ", pageTable)

    # Set up the aging buffer to track the age of each page
    # Aging buffer - This is a set of R buffers
    # We can't keep them in the pageTable since the hardware is
    # supposed to update the pageTable R bit on every reference
    # This is a software addition that every interupt (which we
    # will define to be every 3 instructions read) we transfer that
    # R bit over here on the left, shifting everyting to the right
    agingBits = 8
    agingR = [0] * numPages
    numInstructions = 0

    # Display the initial page table and aging buffer
    displayPageTable(pageTable, decoder, agingR)

    # Loop through the memory accesses
    for memAccess in memAccesses:
        print("-----------------------------------------------------------")
        numInstructions += 1

        # Pull apart the memory access
        process, command, virMemLoc = memAccess.split()
        print("Command: ", command, "  Virtual Memory Location: ", virMemLoc)

        # Get the page number and offset
        virMemLoc = int(virMemLoc)
        pageNum = virMemLoc >> pageBits  # or = virMemLoc / pageSize
        offset = virMemLoc & (pageSize-1)

        print("  pageNum: ", pageNum, "  offset: ", offset)

        # Break up the pieces of the entry
        # Note that if present is false, the other bits are meaningless
        present = decoder.getPresent(pageTable[pageNum])
       
        # Check if the page is in the page table
        if present:
            # Page is loaded so get the frame number
            frameNum = decoder.getFrameNum(pageTable[pageNum])

        else:
            # Page is not loaded so load it
            print(" *** Page Fault ***")

            # There could be a free frame available
            if len(freeFrames) > 0:
                frameNum = freeFrames.pop(0)
                
            else:
                # No free frames so we need to replace one
                # We will use the aging replacement policy
                
                # This selects the oldest referenced page that is present in the page table
                # Note that if there are two pages with the same age, 
                #   the one with the lowest frame number is selected
                pageSelected = 0
                for i in range(numPages):
                    # Note that we only care about present pages
                    pres = decoder.getPresent(pageTable[i])
                    if pres:
                        if agingR[i] < agingR[pageSelected]:
                            pageSelected = i
                        elif (agingR[i] == agingR[pageSelected]) and (decoder.getFrameNum(pageTable[i]) < decoder.getFrameNum(pageTable[pageSelected])):
                            pageSelected = i

                # Get the frame number from the selected replacement page
                # This is the frame we will put the new data into
                frameNum = decoder.getFrameNum(pageTable[pageSelected])
               
                # Unload the old data
                # Note this might require a write back to disk if modified
                # And will always include a modification of the pageTable
                oldModified = decoder.getModified(pageTable[pageSelected])
                if oldModified:
                    print("    Writing data from frame ", frameNum, " back to disk page ", pageSelected)
        
                # Erase the old pageTable entry
                print("    Unloading old data from frame ", frameNum, " to disk page ", pageSelected)
                pageTable[pageSelected] = 0
                agingR[pageSelected] = 0

            # Modify the process pageTable for the new pageTable entry
            # This happens whether we loaded a new page or replaced an old one
            pageTable[pageNum] = decoder.replaceFrameNum(pageTable[pageNum], frameNum)
            pageTable[pageNum] = decoder.setPresent(pageTable[pageNum])
            agingR[pageNum] = pow(2,agingBits) - 1 # Bring it in high
            print("    Loading new data from disk page ", pageNum, " to frame ", frameNum)


        # At this point we know the page is in a frame
        # It either already was or we just loaded it in   
        # Calculate the physical address
        phyMemLoc = (frameNum << pageBits) | offset
        print("--> Physical Location:", phyMemLoc)

        # Update the pageTable entry reference bit
        pageTable[pageNum] = decoder.setReferenced(pageTable[pageNum])

        # If the command is a write, update the modified bit
        if command == 'w':
            pageTable[pageNum] = decoder.setModified(pageTable[pageNum])


        # Update the aging buffer
        # This is a software addition that every interupt (which we
        # will define to be every 3 instructions read) we transfer that
        # R bit over here on the left, shifting everyting to the right
        if numInstructions % 3 == 0:
            print(" ***Aging Buffer Update***")
            for i in range(numPages):
                # Move the bits to the right
                agingR[i] = agingR[i] >> 1

                # If the R bit is set in the pageTable, set the leftmost bit
                #   and clear it from the pageTable
                ref = decoder.getReferenced(pageTable[i])
                if ref == 1:
                    agingR[i] = agingR[i] | (1 << (agingBits-1))
                    pageTable[i] = decoder.clearReferenced(pageTable[i])


        # Display the page table and aging buffer each time
        displayPageTable(pageTable, decoder, agingR)
    

if __name__ == "__main__":
    main()