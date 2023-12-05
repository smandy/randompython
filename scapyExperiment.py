from scapy.all import *
pcap = rdpcap('http.cap')

ips = set([(p[IP].fields['src'], p[IP].fields['dst']) for p in pcap if p.haslayer(IP) ])

# http://www.netresec.com/?page=Blog&month=2012-11&post=Convert-Endace-ERF-capture-files-to-PCAP
# http://www.secdev.org/projects/scapy/doc/usage.html

if 0:
    for i, x in enumerate(pcap[:5]):
        print i, "#" * 80
        #x.show()
        x.show()
        #hexdump(x)

"""
http://itgeekchronicles.co.uk/2013/10/21/scapy-pcap-2-streams/

"""
        
sessions = pcap.sessions()
eyeThames = sessions.items()
        
for i, (q,v) in enumerate(eyeThames):
    print i, q
    print v.summary()

if 0:
    for x in eyeThames[4][1]:
        x.show()
    
def session_extractor(p):
    sess = "Other"
    if 'Ether' in p:
        if 'IP' in p:
            if 'TCP' in p:
                a = p.sprintf('%IP.src% %r,TCP.sport%')
                b = p.sprintf('%IP.dst% %r,TCP.dport%')
                sess = "%s <-> %s" % tuple(sorted( [a,b]))
                #sess = p.sprintf("TCP %IP.src%:%r,TCP.sport% > %IP.dst%:%r,TCP.dport%")
            elif 'UDP' in p:
                sess = p.sprintf("UDP %IP.src%:%r,UDP.sport% > %IP.dst%:%r,UDP.dport%")
            elif 'ICMP' in p:
                sess = p.sprintf("ICMP %IP.src% > %IP.dst% type=%r,ICMP.type% code=%r,ICMP.code% id=%ICMP.id%")
            else:
                sess = p.sprintf("IP %IP.src% > %IP.dst% proto=%IP.proto%")
        elif 'ARP' in p:
            sess = p.sprintf("ARP %ARP.psrc% > %ARP.pdst%")
        else:
            sess = p.sprintf("Ethernet type=%04xr,Ether.type%")
    return sess
