import os
from matplotlib import pyplot as plt
import numpy as np

dir_path = "./fifo_out"
data = {}

def plot_batch(file, name):
    push_cnt = file["push"]
    pop_cnt = file["pop"]
    duration_cnt = file['pkt_dur'] 
    
    push_time = [d['cyc_cnt'] for d in push_cnt]
    pop_time = [d['cyc_cnt'] for d in pop_cnt]

    fig = plt.figure()
    ax = fig.add_subplot(111)    # The big subplot
    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234)
    ax5 = fig.add_subplot(235)
    # Turn off axis lines and ticks of the big subplot
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
    
    plot_hist(duration_cnt, "Time(Cycles) in FIFO for each Packet", ax1)
    plot_hist([j-i for i, j in zip(push_time[:-1], push_time[1:])], "Cycle Seperation between Successive Push", ax2)
    plot_hist([j-i for i, j in zip(pop_time[:-1], pop_time[1:])], "Cycle Seperation between Successive Pop", ax3)
    plot_hist([d['fill_cnt'] for d in push_cnt],"Depth of FIFO at each Push", ax4)
    plot_hist([d['fill_cnt'] for d in pop_cnt],"Depth of FIFO at each Pop", ax5)

    ax.set_title(name)

    
def plot_hist(list,name, ax):
    if len(list) == 0:
        return
    q25, q75 = np.percentile(list, [25, 75])
    bin_width = 2 * (q75 - q25) * len(list) ** (-1/3)
    bins = np.histogram_bin_edges(np.array(list), bins='auto')
    #bins = np.round(bins)
    #bins = bins.astype(int)
    #print("Freedman–Diaconis number of bins:", bins)
    #fig, ax = plt.subplots()
    counts, edges, bars = ax.hist(list, edgecolor="white", bins=bins)
    print(bins)
    ax.bar_label(bars)
    # Set the ticks to be at the edges of the bins.
    ax.set_xticks(bins.astype(int))
    ax.set_xlabel(name)

def proc_data(f, name):
    pkt_push_cyc_cnt = []
    pkt_pop_cyc_cnt = []
    push_cnt = []
    pop_cnt = []
    duration_cnt = []
    while line := f.readline():
        while proc_line := f.readline():
            if proc_line.find('+ PKT PUSH')!=-1:
                pkt_push_cyc_cnt.append(int(proc_line[proc_line.find('cycle_count')+len('cycle_count:       '):-1]))
            elif proc_line.find('- PKT POP')!=-1:
                pkt_pop_cyc_cnt.append(int(proc_line[proc_line.find('cycle_count')+len('cycle_count:       '):-1]))
            elif proc_line.find('FIFO duration')!= -1:
                
                duration_cnt.append(int(proc_line[proc_line.find('FIFO duration:')+len('FIFO duration:       '):-1]))
            elif proc_line.find('PUSH:')!=-1:
                push_cnt.append({'cyc_cnt':int(proc_line[proc_line.find('cycle_count')+len('cycle_count:       '):proc_line.find(',')]),'fill_cnt':int(proc_line[(proc_line.find('fill_count')+len('fill_count:          ')):-1])})
            elif proc_line.find('POP:')!=-1:
                pop_cnt.append({'cyc_cnt':int(proc_line[proc_line.find('cycle_count')+len('cycle_count:       '):proc_line.find(',')]),'fill_cnt':int(proc_line[(proc_line.find('fill_count')+len('fill_count:          ')):-1])})      
    diction = {'pkt_push':pkt_push_cyc_cnt, 'pkt_pop':pkt_pop_cyc_cnt, 'push':push_cnt, 'pop':pop_cnt, 'pkt_dur':duration_cnt}
    data[name] = diction

for filename in os.listdir(dir_path):
    print(filename)
    
    with open(os.path.join(dir_path, filename), 'r') as f:
        idx1 = filename.find("partition_1.")+len("partition_1.")
        idx2 = filename.find(".FIFO",idx1)
        print(idx1,idx2)
        name = filename[idx1:idx2]
        print(name)
        proc_data(f,name)
        
plt.clf()
for file in data:
    plot_batch(data[file], file)
plt.show()
        
        
