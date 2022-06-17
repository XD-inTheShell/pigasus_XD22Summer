
from matplotlib import pyplot as plt
import numpy as np

path = "/Users/xiyingdeng/Library/Mobile\ Documents/com\~apple\~CloudDocs/Desktop/yesxiying/Research/Pigasus/"
filename = "out.txt"
f = open("./out.txt", "r")

pkt_push_cyc_cnt = []
pkt_pop_cyc_cnt = []
push_cnt = []
pop_cnt = []
duration_cnt = []

def plot_hist(list,name):
    q25, q75 = np.percentile(list, [25, 75])
    bin_width = 2 * (q75 - q25) * len(list) ** (-1/3)
    bins = np.histogram_bin_edges(np.array(list), bins='auto')
    #bins = np.round(bins)
    #bins = bins.astype(int)
    #print("Freedman–Diaconis number of bins:", bins)
    fig, ax = plt.subplots()
    counts, edges, bars = ax.hist(list, edgecolor="white", bins=bins)
    print(bins)
    ax.bar_label(bars)
    # Set the ticks to be at the edges of the bins.
    ax.set_xticks(bins.astype(int))
    ax.set_xlabel(name)
    
    

while line := f.readline():
    if line.find('Finish PKT emptylist init')!=-1:
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
    else: continue
push_time = [d['cyc_cnt'] for d in push_cnt]
pop_time = [d['cyc_cnt'] for d in pop_cnt]
plt.clf()
plot_hist(duration_cnt, "Time(Cycles) in FIFO for each Packet")
plot_hist([j-i for i, j in zip(push_time[:-1], push_time[1:])], "Time(Cycles) Seperation between Successive Push")
plot_hist([j-i for i, j in zip(pop_time[:-1], pop_time[1:])], "Time(Cycles) Seperation between Successive Pop")
plot_hist([d['fill_cnt'] for d in push_cnt],"Depth of FIFO at each Push")
plot_hist([d['fill_cnt'] for d in pop_cnt],"Depth of FIFO at each Pop")
plt.show()



    
