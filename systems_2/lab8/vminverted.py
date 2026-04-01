import math

class IPTEntry:
    # Represents one physical frame's metadata
    def __init__(self):
        self.present = 0        # Always 1 when in use
        self.modified = 0
        self.referenced = 0
        self.process = -1       # Which process owns this frame?
        self.page = -1          # Which virtual page?
    
    def __repr__(self):
        if self.present:
            return f"(proc={self.process}, page={self.page}, M={self.modified}, R={self.referenced})"
        else:
            return "(free)"

def readFile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    virBits = int(lines[0].split()[0])
    phyBits = int(lines[0].split()[1])
    pageBits = int(lines[0].split()[2])

    numProcesses = int(lines[1])
    lines = lines[2:]

    return virBits, phyBits, pageBits, numProcesses, lines

def displayIPT(ipt, agingR):
    print("\nInverted Page Table (Frame → Process:Page):")
    print("Frame\tP\tR\tM\tProcess\tPage\tAging")
    for i, e in enumerate(ipt):
        if e.present:
            print(f"{i}\t1\t{e.referenced}\t{e.modified}\t{e.process}\t{e.page}\t{agingR[i]}")
        else:
            print(f"{i}\t0\t-\t-\t-\t-\t-")

def main(filename):

    virBits, phyBits, pageBits, numProcesses, memAccesses = readFile(filename)

    virMemSize = 2 ** virBits
    phyMemSize = 2 ** phyBits
    pageSize = 2 ** pageBits

    numFrames = phyMemSize // pageSize
    numPages = virMemSize // pageSize

    print("Virtual Memory Size:", virMemSize)
    print("Physical Memory Size:", phyMemSize)
    print("Page Size:", pageSize)
    print("Number of Pages per process:", numPages)
    print("Number of Frames:", numFrames)

    # Our single inverted page table
    ipt = [IPTEntry() for _ in range(numFrames)]

    # Free frames list
    freeFrames = [i for i in range(numFrames)]

    # Aging metadata for each frame
    agingBits = 8
    agingR = [0] * numFrames

    numInstructions = 0

    displayIPT(ipt, agingR)

    for memAccess in memAccesses:
        print("\n----------------------------------------------------")
        numInstructions += 1

        processNum, command, virAddr = memAccess.split()
        processNum = int(processNum)
        virAddr = int(virAddr)

        pageNum = virAddr >> pageBits
        offset = virAddr & (pageSize - 1)

        print("Process:", processNum, "Command:", command, "Virtual Address:", virAddr)
        print("Page:", pageNum, "Offset:", offset)

        # SEARCH inverted page table for (proc,page)
        found = False
        frameNum = -1

        for i, entry in enumerate(ipt):
            if entry.present == 1 and entry.process == processNum and entry.page == pageNum:
                found = True
                frameNum = i
                break

        if found:
            print("Page found in frame", frameNum)

        else:
            print(" *** PAGE FAULT ***")

            # Case 1: Free frame available
            if len(freeFrames) > 0:
                frameNum = freeFrames.pop(0)
                print("Using free frame", frameNum)

            # Case 2: Need replacement using aging
            else:
                print("Selecting victim using aging algorithm…")
                oldestAge = min(agingR)
                frameNum = agingR.index(oldestAge)
                victim = ipt[frameNum]

                print(f"Evicting process {victim.process} page {victim.page} from frame {frameNum}")

                if victim.modified == 1:
                    print(" → Writing modified page to disk")

                # Clear old entry
                ipt[frameNum] = IPTEntry()

            # Load new page
            newEntry = IPTEntry()
            newEntry.present = 1
            newEntry.modified = 0
            newEntry.referenced = 1
            newEntry.process = processNum
            newEntry.page = pageNum

            ipt[frameNum] = newEntry
            agingR[frameNum] = (2 ** agingBits) - 1  # Initialize age high

            print(f"Loaded process {processNum} page {pageNum} into frame {frameNum}")

        # Update bits
        ipt[frameNum].referenced = 1
        if command == "w":
            ipt[frameNum].modified = 1

        # Physical address
        phyAddr = (frameNum << pageBits) | offset
        print("--> Physical Address:", phyAddr)

        # Aging update every 3 instructions
        if numInstructions % 3 == 0:
            print(" *** AGING UPDATE ***")
            for i in range(numFrames):
                if ipt[i].present:
                    agingR[i] >>= 1
                    if ipt[i].referenced:
                        agingR[i] |= (1 << (agingBits - 1))
                        ipt[i].referenced = 0

        displayIPT(ipt, agingR)

if __name__ == "__main__":
    main("test_inverted.txt")
