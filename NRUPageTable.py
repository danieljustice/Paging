class nru_table:
    def __init__(self, tracefile_path, num_frames = 8):
        self.refresh_rate = 5
        self.max_frames = num_frames
        self.frames = []
        self.active_frames = 0
        self.pageFaults = 0
        self.diskWrites = 0
        self.lineNumber = 0
        self.memAccesses = 0
        tracefile = open(tracefile_path, mode='r')
        self.run_sim(tracefile)
        tracefile.close()



    def run_sim(self, tracefile):
        for line in tracefile:
            self.lineNumber+=1
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
                #(address, Referenced, Clean)
                self.frames.append((address, True, False))
                self.active_frames += 1
                #position in the array of frames is 1 less than active_frames
                frame_position = self.active_frames-1
            else:
                #if there was no empty frame
                index_to_replace = self.determine_nru()
                #if was dirty, then write to disk
                if(self.frames[index_to_replace][2] == True):
                    self.diskWrites += 1
                    print(address, " page fault - evict dirty")
                else:
                    print(address, " page fault - evict clean")
                #replaces old frame with new address and priority
                self.frames[index_to_replace] = (address, True, False)
                frame_position = index_to_replace
        else:
            print(address, " hit")       
            #reset frames referenced bit to true
            for frame in self.frames:
                if frame[0] == address:
                    cur_frame_index = self.frames.index(frame)
                    self.frames[cur_frame_index] = (address,True,self.frames[cur_frame_index][2])
        #refresh statements
        if self.lineNumber%self.refresh_rate == 0:
            for index in range(0, self.active_frames):
                #based on refresh rate, set each referenced boolean to 0
                self.frames[index] = (self.frames[index][0], False, self.frames[index][2]) 
        return frame_position


    def determine_nru(self):
        n_ref_clean = []
        n_ref_dirty = []
        ref_clean = []
        ref_dirty = []
        for frame in self.frames:
            if(frame[1] == False and frame[2] == False):
                n_ref_clean.append(frame)
            if(frame[1] == False and frame[2] == True):
                n_ref_dirty.append(frame)
            if(frame[1] == True and frame[2] == False):
                ref_clean.append(frame)
            if(frame[1] == True and frame[2] == True):
                ref_dirty.append(frame)

        if n_ref_clean:
            return self.frames.index(n_ref_clean[0])
        elif n_ref_dirty:
            return self.frames.index(n_ref_dirty[0])
        elif ref_clean:
            return self.frames.index(ref_clean[0])
        elif ref_dirty[0]:
            return self.frames.index(ref_dirty[0])
        else:
            print("What?")
            return None