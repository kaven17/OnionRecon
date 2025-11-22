# generate_synthetic.py
import csv, time, random
now = time.time()
with open("data/synthetic_events.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["capture_file","timestamp","src_ip","dst_ip","src_port","dst_port","pkt_len","flow_id"])
    for i in range(200):
        ts = now + i*0.05 + random.random()*0.02
        src = "10.0.0.5"
        dst = f"93.184.216.{random.randint(1,255)}"
        s = random.randint(1000,60000)
        d = 443
        ln = random.randint(60,1500)
        flow = f"{src}:{s}->{dst}:{d}"
        w.writerow(["synthetic.pcap", ts, src, dst, s, d, ln, flow])
print("synthetic CSV written")
