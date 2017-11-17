from OptimalPageTable import opt_table as opt_table
from RandomPageTable import rand_table as rand_table
from NRUPageTable import nru_table as nru_table
from ClockPageTable import clock_table as clock_table
if __name__ == '__main__':

    # opt = opt_table("swim.trace", 9)
    # print("Algorithm: Optimal")
    # print("Number of frames: ", opt.max_frames)
    # print("Total memory accesses: ", opt.memAccesses)
    # print("Total page faults: " , opt.pageFaults)
    # print("Total writes to disk: " , opt.diskWrites)

    # randtable = rand_table("swim.trace", 8)
    # print("Algorithm: Random")
    # print("Number of frames: ", randtable.max_frames)
    # print("Total memory accesses: ", randtable.memAccesses)
    # print("Total page faults: " , randtable.pageFaults)
    # print("Total writes to disk: " , randtable.diskWrites)

    # nrutable = nru_table("swim.trace", 8)
    # print("Algorithm: NRU")
    # print("Number of frames: ", nrutable.max_frames)
    # print("Total memory accesses: ", nrutable.memAccesses)
    # print("Total page faults: " , nrutable.pageFaults)
    # print("Total writes to disk: " , nrutable.diskWrites)
    
    clocktable = clock_table("swim.trace", 8)
    print("Algorithm: Clock")
    print("Number of frames: ", clocktable.max_frames)
    print("Total memory accesses: ", clocktable.memAccesses)
    print("Total page faults: " , clocktable.pageFaults)
    print("Total writes to disk: " , clocktable.diskWrites)