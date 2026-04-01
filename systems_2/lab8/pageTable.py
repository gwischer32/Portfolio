# standard virtual memory page table implementation

# This is a basic implementation of a page table
#   with aging as the replacement policy
# It includes no TLB, multilevel or inverted tables
# It works for multiple processes

# The format of a page table entry is:
#   ---Mbit Rbit Pbit frame#

import math

# This is a helper class that decodes any page table entry given to it
#   so we don't have to have all the bit manipulation in the main code
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
    


def displayPageTable(pageTables, decoder, agingR):

    print("\nPage Tables (with associated aging status):")
    for i in range(len(pageTables)):
        print("\nProcess ", i)
        print("page#\tmod\tref\tpresent\tframe#\taging")
        for j in range(len(pageTables[i])):
            pageTableEntry = pageTables[i][j]

            m = decoder.getModified(pageTableEntry)
            r = decoder.getReferenced(pageTableEntry)
            p = decoder.getPresent(pageTableEntry)
            pf = decoder.getFrameNum(pageTableEntry)

            if p:
                print(j, ":\t", m, "\t", r, "\t", p, "\t", pf, "\t", (agingR[pf]))
            else:
                print(j, ":\t", "-", "\t", "-", "\t", p, "\t", "-", "\t", "-")
 
def readFile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    # First line is the number of bits for things
    #  Virtual Address, Physical Address, Page Size
    virBits = int(lines[0].split()[0])
    phyBits = int(lines[0].split()[1])
    pageBits = int(lines[0].split()[2])

    # Second line is the number of processes
    numProcesses = int(lines[1])
    
    # Remove the first two lines
    lines = lines[2:]

    return virBits, phyBits, pageBits, numProcesses, lines

def main(filename):
    virBits, phyBits, pageBits, numProcesses, memAccesses = readFile(filename)

    # Calculate sizes based on the number of bits
    virMemSize = 2 ** virBits
    phyMemSize = 2 ** phyBits
    pageSize = 2 ** pageBits

    print("INITIAL PAGETABLE SETUP:")
    print("  Virtual Mememory Size:", virMemSize)
    print("  Physical Memory Size:", phyMemSize)
    print("  Page Size:", pageSize)

    # Compute values based on the info above
    # These should all be powers of 2 so the divides will be even
    numFrames = phyMemSize // pageSize
    numPages = virMemSize // pageSize
    frameBits = int(math.log2(numFrames))

    # Create the helper to decode the page table entries
    decoder = PageTableDecoder(frameBits)

    print("  Number of Pages:", numPages)
    print("  Number of Frames:", numFrames)
    print("  FrameBits:", frameBits)
    print("  Number of processes", numProcesses)

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
    pageTables = []
    for i in range(numProcesses):
        pageTables.append([0] * numPages)
    print("Page Tables: ", pageTables)

    # Set up the aging buffer to track the age of each page loaded in a frame
    # Aging buffer - This is a set of R buffers
    # We can't keep them in the pageTable since the hardware is
    # supposed to update the pageTable R bit on every reference
    # This is a software addition that every interupt (which we
    # will define to be every 3 instructions read) we transfer that
    # R bit over here on the left, shifting everyting to the right
    # We attach the aging information to each frame since it is only
    #  used in the aging replacement policy for active frames
    agingBits = 8
    agingR = [0] * numFrames
    numInstructions = 0

    # Display the initial page table and aging buffer
    displayPageTable(pageTables, decoder, agingR)

    # Loop through the memory accesses
    for memAccess in memAccesses:
        print("-----------------------------------------------------------")
        numInstructions += 1

        # Pull apart the memory access
        processNum, command, virMemLoc = memAccess.split()
        print("Process:", processNum, " Command:", command, " Virtual Memory Location:", virMemLoc)

        # Get the page number and offset
        processNum = int(processNum)
        virMemLoc = int(virMemLoc)
        pageNum = virMemLoc >> pageBits  # or = virMemLoc / pageSize
        offset = virMemLoc & (pageSize-1)

        print("  pageNum: ", pageNum, "  offset: ", offset)

        # Determine if the page is present in a frame
        # Note that if present is false, the other bits are meaningless
        present = decoder.getPresent(pageTables[processNum][pageNum])
       
        # Check if the page is in the page table
        if present:
            # Page is loaded so get the frame number
            frameNum = decoder.getFrameNum(pageTables[processNum][pageNum])

        else:
            # Page is not loaded so load it
            print(" *** Page Fault ***")

            # There could be a free frame available
            if len(freeFrames) > 0:
                frameNum = freeFrames.pop(0)
                
            else:
                # No free frames so we need to replace one
                # We will use the aging replacement policy
                # We use a global aging buffer for all processes
                #   so we could kick out a page from any process
                #   If there is a tie in the aging, we will kick out the
                #   process with the lower number
                
                # This selects the oldest referenced page that is present in the page table
                # We still go through it starting from the page tables since the frames
                #   do not know what process they are associated with
                # Note that if there are two pages with the same age, 
                #   the one with the lowest frame number is selected
                processSelected = -1
                pageSelected = -1
                lowestAge = pow(2, agingBits) + 1;  # highest possible
                for i in range(numProcesses):
                    for j in range(numPages):
                        # Note that we only care about present pages
                        pres = decoder.getPresent(pageTables[i][j])
                        if pres:
                            fn = decoder.getFrameNum(pageTables[i][j])
                            if agingR[fn] < lowestAge:
                                processSelected = i
                                pageSelected = j
                                lowestAge = agingR[fn]
                            elif (agingR[fn] == lowestAge) and (fn < decoder.getFrameNum(pageTables[processSelected][pageSelected])):
                                processSelected = i
                                pageSelected = j
                                lowestAge = agingR[fn]

                # Get the frame number from the selected replacement page
                # This is the frame we will put the new data into
                frameNum = decoder.getFrameNum(pageTables[processSelected][pageSelected])
               
                # Unload the old data
                # Note this might require a write back to disk if modified
                # And will always include a modification of the pageTable
                oldModified = decoder.getModified(pageTables[processSelected][pageSelected])
                if oldModified:
                    print("    Writing modified data...")
        
                # Erase the old pageTable entry
                print("    Removing page", pageSelected, "of process", processSelected, "from frame", frameNum)
                pageTables[processSelected][pageSelected] = 0
                agingR[frameNum] = 0
              
            # Modify the process pageTable for the new pageTable entry
            # This happens whether we loaded a new page or replaced an old one
            pageTables[processNum][pageNum] = decoder.replaceFrameNum(pageTables[processNum][pageNum], frameNum)
            pageTables[processNum][pageNum] = decoder.setPresent(pageTables[processNum][pageNum])

            # And the aging buffer
            agingR[frameNum] = pow(2,agingBits) - 1 # Bring it in high
            print("    Loading page", pageNum, "of process", processNum, "to frame", frameNum)


        # At this point we know the page is in a frame
        # It either already was or we just loaded it in   
        # Calculate the physical address
        phyMemLoc = (frameNum << pageBits) | offset
        print("--> Physical Location:", phyMemLoc)

        # Update the pageTable entry reference bit
        pageTables[processNum][pageNum] = decoder.setReferenced(pageTables[processNum][pageNum])

        # If the command is a write, update the modified bit
        if command == 'w':
            pageTables[processNum][pageNum] = decoder.setModified(pageTables[processNum][pageNum])


        # Update the aging buffer
        # This is a software addition that every interupt (which we
        # will define to be every 3 instructions read) we transfer that
        # R bit over here on the left, shifting everyting to the right
        if numInstructions % 3 == 0:
            print(" ***Aging Buffer Update***")

            # We can't just run through all the frames -- well we can
            #   to do the shifting.  But we then need the ref bit on the page
            #   and we have no way of mapping backwards to the page from the frame
            # So we instead access the frames through the pageTables
            for i in range(numProcesses):
                for j in range(numPages):
                    # Note that we only care about present pages
                    pres = decoder.getPresent(pageTables[i][j])
                    if pres:
                        fn = decoder.getFrameNum(pageTables[i][j])

                        # Move everything to the right 1 bit
                        agingR[fn] = agingR[fn] >> 1

	                    # Add in the R hardware bit to the aging on the left
                        ref = decoder.getReferenced(pageTables[i][j])
                        if ref == 1:
                            agingR[fn] = agingR[fn] | (1 << (agingBits-1))
                             
	                        # Wipe out the R hardware bit
                            pageTables[i][j] = decoder.clearReferenced(pageTables[i][j])


        # Display the page table and aging buffer each time
        displayPageTable(pageTables, decoder, agingR)
    

if __name__ == "__main__":
    #main("testCases/inputOne.txt")
    main("testCases/inputTwo.txt")