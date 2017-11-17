class opt_table:
    def __init__(self, tracefile_path, num_frames = 8):
        self.max_frames = num_frames
        self.frames = []
        self.active_frames = 0
        self.pageFaults = 0
        self.diskWrites = 0
        self.lineNumber = 0
        self.memAccesses = 0
        tracefile = open(tracefile_path, mode='r')
        #print("starting")
        self.address_priority = self.prioritize_addresses(tracefile)
        #print("Done prioritizing")
        tracefile.close()
        tracefile = open(tracefile_path, mode='r')
        self.run_sim(tracefile)
        tracefile.close()



    def prioritize_addresses(self, file):
        """Takes in a file and returns a dictionary of addresses and their priority"""
        #I dont want duplicates and dont care about order right now
        address_freq_dict = {}
        address_priority_dict = {}
        for line in file:
            #first part is the address, second part is the action, we only want the address
            cur_address = line.split()[0]
            if cur_address in address_freq_dict:
                #if it exists in dict, increase freq
                address_freq_dict[cur_address] +=1
            else:
                #if not in dict, add it and set freq to 1
                address_freq_dict[cur_address] = 1
        #we are going to prioritize
        reverse_frequency_add_arr = sorted(address_freq_dict, key=address_freq_dict.get, reverse=True)
        #insert each address into the dictionary mapped to its priority
        for index in range(0, len(reverse_frequency_add_arr)):
            address_priority_dict[reverse_frequency_add_arr[index]] = index

        return address_priority_dict

    def run_sim(self, tracefile):
        for line in tracefile:
            self.memAccesses += 1
            address, mode = line.split()
            if mode == 'R':
                self.read(address)
            elif mode == 'W':
                self.write(address)
            else:
                print(mode + " is not an acceptable mode.")

    def read(self, address):
        self.replace(address)
        return None

    def write(self, address):            
        frame_position = self.replace(address)
        temp_frame = self.frames[frame_position] 
        temp_frame = (temp_frame[0], temp_frame[1], True)
        self.frames[frame_position] = temp_frame
        return None

    def replace(self, address):
        frame_position = -1
        if not any(address in frame for frame in self.frames):
            #if address not currently in active frames, then it is a page fault, time to handle it
            self.pageFaults += 1
            #if address is not currently an active frame
            if self.active_frames < self.max_frames:
                #if there is an open frame, then insert the address as a tuple with its priority
                print(address, " page fault - no eviction")
                self.frames.append((address, self.address_priority[address], False))
                self.active_frames += 1
                #position in the array of frames is 1 less than active_frames
                frame_position = self.active_frames-1
            else:
                least_priority_frame = max(self.frames, key=lambda frame: frame[1])
                index_to_replace = self.frames.index(least_priority_frame)
                #if was dirty, then write to disk
                if(least_priority_frame[2] == True):
                    self.diskWrites += 1
                    print(address, " page fault - evict dirty")
                else:
                    print(address, " page fault - evict clean")
                #replaces old frame with new address and priority
                self.frames[index_to_replace] = (address, self.address_priority[address], False)
                frame_position = index_to_replace
        else:
            print(address, " hit")        
        return frame_position