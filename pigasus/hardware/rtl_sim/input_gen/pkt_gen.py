#! /usr/bin/env python3
import sys
import time
import csv
from scapy.all import *

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy import stats
import random
import copy
import math

def pr_inorder_match(pkt_num,pkt_len,match,initial_seq,nomatch_start,nomatch_end):
    outpkt = []
    payload_len = pkt_len - 40 - 18
    pattern = b'\xFF\xFF\xFA\xA5\xF8\xFB\x22\x88'
    #pattern = b'\xFA\xA5\xF8\xFB\x22\x88\xFF\xFF'
    for i in range(0,pkt_num):
        pkt = Ether()/IP()/TCP()/Raw()
        pkt[Ether].dst = "02:00:00:00:00:00"
        pkt[Ether].src = "ab:cd:ef:00:00:00"
        pkt[IP].src = "10.0.0.1"
        pkt[IP].dst = "192.168.1.2"
        pkt[IP].ihl = 5
        pkt[IP].id = i
        pkt[TCP].dataofs = 5
        pkt[TCP].flags = 'P'
        pkt[TCP].sport = 1025
        pkt[TCP].dport = 1024
        pkt[IP].len = 40 + payload_len

        #print (type(pkt[Raw].load))
        if i in range(nomatch_start,nomatch_end):
            pkt[Raw].load = b'\xFF'*payload_len
        else:
            if i%match == 0:
                pkt[Raw].load = pattern+ (b'\xff'*(payload_len-8))
            else:
                #pkt[Raw].load = "\xff".encode('ascii','backslashreplace')*payload_len
                #pkt[Raw].load = chr(255).encode('utf-8')*payload_len
                pkt[Raw].load = b'\xFF'*payload_len
        #print (pkt[Raw].load)
        pkt[TCP].seq = initial_seq + i*payload_len
        #pkt.show()

        outpkt.append(pkt)

    return outpkt


pkt_num = 1000
nomatch_start = 500
nomatch_end = 800
pkt_len = 1500

match = 1
#one generated pcap cannot be too big. Generate multiple smaller pcap instead
for i in range(0,1):
    filename = "pr_m"+str(match)+"_"+str(pkt_num)+"_"+str(nomatch_start)+"-"+str(nomatch_end)+"_"+str(i)+".pcap"
    pkts = pr_inorder_match(pkt_num,pkt_len,match,i*pkt_num*(pkt_len-40-18),nomatch_start,nomatch_end)
    print (filename)
    wrpcap(filename,pkts)


