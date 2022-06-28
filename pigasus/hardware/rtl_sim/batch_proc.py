import os
from matplotlib import pyplot as plt
import numpy as np

import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))

dir_path = "./fifo_out"
out_path = "./graph_out"
data = {}

def plot_batch(file, name):
    push_cnt = file["push"]
    pop_cnt = file["pop"]
    duration_cnt = file['pkt_dur'] 
    
    push_time = [d['cyc_cnt'] for d in push_cnt]
    pop_time = [d['cyc_cnt'] for d in pop_cnt]

    pkt_push_time = file['pkt_push']
    pkt_pop_time = file['pkt_pop']
    
    # Plot flit histogram
    fig1 = plt.figure()
    fig1.set_size_inches(22,10)
    ax = fig1.add_subplot(111)    # The big subplot
    ax1 = fig1.add_subplot(221)
    ax2 = fig1.add_subplot(222)
    ax3 = fig1.add_subplot(223)
    ax4 = fig1.add_subplot(224)
    
    # Turn off axis lines and ticks of the big subplot
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
    
    
    plot_hist_auto([j-i for i, j in zip(push_time[:-1], push_time[1:])], "Cycles between Push", ax1)
    plot_hist_auto([j-i for i, j in zip(pop_time[:-1], pop_time[1:])], "Cycles between Pop", ax2)
    plot_hist_auto([d['fill_cnt'] for d in push_cnt],"Depth at each Push", ax3)
    plot_hist_auto([d['fill_cnt'] for d in pop_cnt],"Depth at each Pop", ax4)

    ax.set_title(name)
    plt.savefig('graph_out/'+'flit*'+name+'.png')
    # Plot pkt histogram
    fig2 = plt.figure()
    fig2.set_size_inches(14,10)
    ax = fig2.add_subplot(111)    
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
    
    ax1 = fig2.add_subplot(221)
    ax2 = fig2.add_subplot(222)
    ax3 = fig2.add_subplot(223)
    ax4 = fig2.add_subplot(224)
    plot_hist(duration_cnt, "Time(Cycles) in FIFO for each Packet", ax1)
    plot_hist([j-i for i, j in zip(pkt_push_time[:-1], pkt_push_time[1:])], "Cycles between Pkt Push", ax2)
    plot_hist([j-i for i, j in zip(pkt_pop_time[:-1], pkt_pop_time[1:])], "Cycles between Pkt Pop", ax3)

    plot_scatter(pkt_push_time,"Time Pkts Enter FIFO",'push',ax4)
    plot_scatter(pkt_pop_time,"Time Pkts Exit FIFO",'pop',ax4)
    
    ax.set_title(name)
    plt.savefig('graph_out/'+'pkt*'+name+'.png')

def plot_scatter(plist,name,leg,ax):
    sct = ax.scatter(list(range(0,len(plist))),plist)
    ax.set_xlabel(name)
    ax.set_ylabel("Time (Cycles)")
    sct.set_label(leg)
    ax.legend()
    
def plot_hist(plist,name, ax):
    
    if len(plist) == 0:
        return
    q25, q75 = np.percentile(plist, [25, 75])
    bin_width = 2 * (q75 - q25) * len(plist) ** (-1/3)
    bins = np.histogram_bin_edges(np.array(plist), bins='auto')
    #bins = np.round(bins)
    #bins = bins.astype(int)
    #print("Freedman–Diaconis number of bins:", bins)
    #fig, ax = plt.subplots()

    if min(plist) == max(plist):
        fixbin = 1
    else:
        fixbin = np.arange(min(plist),max(plist)+1,((max(plist)-min(plist))/10))

    bars = ax.hist(plist, edgecolor="white", bins=fixbin)
    
    if min(plist) != max(plist):
        for i in range(len(fixbin)-1):
            ax.text(bars[1][i],bars[0][i],str(int(bars[0][i])))

    else:
        print(bars)
        ax.text((bars[1][0]+bars[1][1])/2,bars[0][0],str(int(bars[0][0])))

    
    # ax.bar_label(bars)
    # Set the ticks to be at the edges of the bins.
    # ax.set_xticks(fixbin)
    ax.set_xlabel(name)

def plot_hist_auto(plist,name, ax):
    
    if len(plist) == 0:
        return
    q25, q75 = np.percentile(plist, [25, 75])
    bin_width = 2 * (q75 - q25) * len(plist) ** (-1/3)
    bins = np.histogram_bin_edges(np.array(plist), bins='auto')
    #bins = np.round(bins)
    #bins = bins.astype(int)
    #print("Freedman–Diaconis number of bins:", bins)
    #fig, ax = plt.subplots()
    bars = ax.hist(plist, edgecolor="white", bins=bins)

    if min(plist) != max(plist):
        for i in range(len(bins)-1):
            ax.text(bars[1][i],bars[0][i],str(int(bars[0][i])))

    else:
        print(bars)
        ax.text((bars[1][0]+bars[1][1])/2,bars[0][0],str(int(bars[0][0])))
    # Set the ticks to be at the edges of the bins.
    ax.set_xticks(bins.astype(int))
    ax.set_xlabel(name)

def proc_data(f, name):
    pkt_push_cyc_cnt = []
    pkt_pop_cyc_cnt = []
    push_cnt = []
    pop_cnt = []
    duration_cnt = []
    print(name)
    while True:
        proc_line = f.readline()
        
        if not proc_line:
            break;
        if proc_line.find('+ PKT PUSH')!=-1:
            pkt_push_cyc_cnt.append(int(proc_line[proc_line.find('cycle_count')+len('cycle_count:'):-1]))
        elif proc_line.find('- PKT POP')!=-1:
            pkt_pop_cyc_cnt.append(int(proc_line[proc_line.find('cycle_count')+len('cycle_count:'):-1]))
        elif proc_line.find('FIFO duration')!= -1:
            
            duration_cnt.append(int(proc_line[proc_line.find('FIFO duration:')+len('FIFO duration:'):-1]))
        elif proc_line.find('PUSH:')!=-1:
            
            p_cnt = {'cyc_cnt':int(proc_line[proc_line.find('cycle_count')+len('cycle_count:'):proc_line.find(',')]),'fill_cnt':int(proc_line[(proc_line.find('fill_count')+len('fill_count:')):-1])}
            
            push_cnt.append(p_cnt)
        elif proc_line.find('POP:')!=-1:
            pop_cnt.append({'cyc_cnt':int(proc_line[proc_line.find('cycle_count')+len('cycle_count:'):proc_line.find(',')]),'fill_cnt':int(proc_line[(proc_line.find('fill_count')+len('fill_count:')):-1])})      
    diction = {'pkt_push':pkt_push_cyc_cnt, 'pkt_pop':pkt_pop_cyc_cnt, 'push':push_cnt, 'pop':pop_cnt, 'pkt_dur':duration_cnt}
    data[name] = diction
    print("end"+name)


isExist = os.path.exists(out_path)
if not isExist:
    os.makedirs(out_path)
for filename in os.listdir(dir_path):
    
    with open(os.path.join(dir_path, filename), 'r') as f:
        idx1 = filename.find("partition_1.")+len("partition_1.")
        idx2 = filename.find(".FIFO",idx1)
        
        name = filename[idx1:idx2]

        proc_data(f,name)
        
plt.clf()
for file in data:
    plot_batch(data[file], file)
    
#plt.show()
        
        
