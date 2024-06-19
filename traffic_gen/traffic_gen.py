import sys
import random
import math
import heapq
from optparse import OptionParser
from custom_rand import CustomRand

class Flow:
	def __init__(self, src, dst, size, t):
		self.src, self.dst, self.size, self.t = src, dst, size, t
	def __str__(self):
		return "%d %d 3 100 %d %.9f"%(self.src, self.dst, self.size, self.t)

def translate_bandwidth(b):
	if b == None:
		return None
	if type(b)!=str:
		return None
	if b[-1] == 'G':
		return float(b[:-1])*1e9
	if b[-1] == 'M':
		return float(b[:-1])*1e6
	if b[-1] == 'K':
		return float(b[:-1])*1e3
	return float(b)

def poisson(lam):
	return -math.log(1-random.random())*lam

if __name__ == "__main__":
	cdf_add=0
	incast_add=0
	port = 80
	parser = OptionParser()
	parser.add_option("-c", "--cdf", dest = "cdf_file", help = "the file of the traffic size cdf", default = "uniform_distribution.txt")
	parser.add_option("-n", "--nhost", dest = "nhost", help = "number of hosts")
	parser.add_option("-l", "--load", dest = "load", help = "the percentage of the traffic load to the network capacity, by default 0.3", default = "0.3")
	parser.add_option("-b", "--bandwidth", dest = "bandwidth", help = "the bandwidth of host link (G/M/K), by default 10G", default = "10G")
	parser.add_option("-t", "--time", dest = "time", help = "the total run time (s), by default 10", default = "10")
	parser.add_option("-o", "--output", dest = "output", help = "the output file", default = "tmp_traffic.txt")
	options,args = parser.parse_args()

	base_t = 0
    
	if not options.nhost:
		print "please use -n to enter number of hosts"
		sys.exit(0)
	nhost = int(options.nhost)
	load = float(options.load)
	bandwidth = translate_bandwidth(options.bandwidth)
	time = float(options.time)*1e9 # translates to ns
	output = options.output
	if bandwidth == None:
		print "bandwidth format incorrect"
		sys.exit(0)

	fileName = options.cdf_file
	file = open(fileName,"r")
	lines = file.readlines()
	# read the cdf, save in cdf as [[x_i, cdf_i] ...]
	cdf = []
	for line in lines:
		x,y = map(float, line.strip().split(' '))
		cdf.append([x,y])

	# create a custom random generator, which takes a cdf, and generate number according to the cdf
	customRand = CustomRand()
	if not customRand.setCdf(cdf):
		print "Error: Not valid cdf"
		sys.exit(0)

	ofile = open(output, "w")
	flow_size=[1,3e3,67e2,14e3,20e3,25e3,30e3,40e3,50e3,60e3,73e3,150e3,200e3,600e3,1e6,15e5,2e6,25e5,5e6,10e6]
	flow_size_incast=[1,150,324,360,400,450,500,550,600,650,700,850,1e3,4e3,7e3,3e4,46e3,8e4,12e4,1e6]
	# generate flows
	avg = customRand.getAvg()
	avg_inter_arrival = 1/(bandwidth*load/8./avg)*1000000000
	avg_cdf_arrival=500000
	avg_incast_arrival=1/(bandwidth*nhost*0.05/8./(500000*60*1))*1e9
	n_flow_estimate = int(time / avg_inter_arrival * nhost)
	n_flow = 0
	t_cdf=int(poisson(avg_cdf_arrival))+base_t
	t_incast=int(poisson(avg_incast_arrival))+base_t
	ofile.write("%d \n"%n_flow_estimate)
	host_list = [(base_t + int(poisson(avg_inter_arrival)), i) for i in range(nhost)]
	heapq.heapify(host_list)
	while len(host_list) > 0:
		t,src = host_list[0]
		if t>t_cdf  and t_incast>t_cdf and  t_cdf<time+base_t :
			src_cdf=random.randint(0, nhost-1)
			dst_cdf=random.randint(0, nhost-1)
			while dst_cdf==src_cdf:
				dst_cdf=random.randint(0, nhost-1)
			size_cdf=flow_size_incast[random.randint(0,19)]
			if cdf_add:
				ofile.write("%d %d 3 100 %d %.9f\n"%(src_cdf, dst_cdf, size_cdf, t_cdf * 1e-9))
				n_flow+=1
			cdf_next_t=int(poisson(avg_cdf_arrival))
			t_cdf+=cdf_next_t
		elif t>t_incast and t_incast<time+base_t:
			for i in range(1):
				dst_incast=random.randint(0, nhost-1)
				for j in range(60):
					src_incast=random.randint(0, nhost-1)
					while src_incast==dst_incast:
						src_incast=random.randint(0, nhost-1)
					if incast_add:
						n_flow+=1
						ofile.write("%d %d 3 100 %d %.9f\n"%(src_incast, dst_incast, 500000, t_incast * 1e-9))
			incast_next_t=int(poisson(avg_incast_arrival))
			t_incast+=incast_next_t	
		else:
			inter_t = int(poisson(avg_inter_arrival))
			new_tuple = (src, t + inter_t)
			dst = random.randint(0, nhost-1)
			while (dst == src):
				dst = random.randint(0, nhost-1)
			if (t + inter_t > time + base_t):
				heapq.heappop(host_list)
			else:
				size = int(customRand.rand())
				#size =random.chioce()
				if size <= 0:
					size = 1
				n_flow += 1;
				ofile.write("%d %d 3 100 %d %.9f\n"%(src, dst, size, t * 1e-9))
				heapq.heapreplace(host_list, (t + inter_t, src))
	ofile.seek(0)
	ofile.write("%d"%n_flow)
	ofile.close()

'''
	f_list = []
	avg = customRand.getAvg()
	avg_inter_arrival = 1/(bandwidth*load/8./avg)*1000000000
	# print avg_inter_arrival
	for i in range(nhost):
		t = base_t
		while True:
			inter_t = int(poisson(avg_inter_arrival))
			t += inter_t
			dst = random.randint(0, nhost-1)
			while (dst == i):
				dst = random.randint(0, nhost-1)
			if (t > time + base_t):
				break
			size = int(customRand.rand())
			if size <= 0:
				size = 1
			f_list.append(Flow(i, dst, size, t * 1e-9))

	f_list.sort(key = lambda x: x.t)

	print len(f_list)
	for f in f_list:
		print f
'''
