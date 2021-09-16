import random
import math

#Given list of worlds
#Generates random info partition
def partition(lst):
	if len(lst)==1:
		return [lst]
	else:
		part=partition(lst[:-1])
		place=random.randint(0,len(part))
		if place==len(part):
			part.append([lst[-1]])
			return part
		else:
			part[place].append(lst[-1])
			return part

#Given a world and an info partition
#Returns chunk the world is contained in
def which_chunk(world, part):
	for chunk in part:
		if world in chunk:
			return chunk

#Given info partition and list of chunk indices
#Returns union of chunks corresponding to indices
def unionchnks(part,chnks):
	union=[]
	for i in chnks:
		union+=part[i]
	return union

#Given event, chunk of agent, opponent's info partition, 
#and list of opponent's possible chunks
#Returns posterior of agent
def posterior(event, chunk, opp_part, opp_chnks):
	post=len(set(event) & (set(chunk) & set(unionchnks(opp_part, opp_chnks)) ))/len(set(chunk) & set(unionchnks(opp_part, opp_chnks)))
	return post

#Given posterior, event, info partition, opponent's
#info partition, and opponent's possible chunks
#Returns possible chunks consistent 
#with reported posterior
def pssblchnks(post, event, part, opp_part, opp_chnks, oldpssblchnks):
	chnks=[]
	for chunk in part:
		if len(set(chunk) & set(unionchnks(opp_part, opp_chnks)))!=0:
			chunk_post=posterior(event, chunk, opp_part, opp_chnks)
		else:
			chunk_post="Undefined"
		if chunk_post==post:
			chnks.append(part.index(chunk))
	return list(set(chnks) & set(oldpssblchnks))

#Given true state of world, event, and
#both agents' information partitions
#Simulates communication process and returns
#list of reported posteriors for both agents
def communicate(world, event, agent_A, agent_B):
	chunk_A=which_chunk(world,agent_A)
	chunk_B=which_chunk(world,agent_B)
	oldpssblchnks_A=range(len(agent_A))
	oldpssblchnks_B=range(len(agent_B))
	A_report=[]
	B_report=[]
	
	posterior_A=posterior(event, chunk_A, agent_B, oldpssblchnks_B)
	A_report.append(posterior_A)
	newpssblchnks_A=pssblchnks(posterior_A, event, agent_A, agent_B, oldpssblchnks_B, oldpssblchnks_A)
	
	posterior_B=posterior(event, chunk_B, agent_A, newpssblchnks_A)
	B_report.append(posterior_B)
	newpssblchnks_B=pssblchnks(posterior_B, event, agent_B, agent_A, newpssblchnks_A, oldpssblchnks_B)

	while (newpssblchnks_A!=oldpssblchnks_A or newpssblchnks_B!=oldpssblchnks_B):
		oldpssblchnks_A=newpssblchnks_A
		oldpssblchnks_B=newpssblchnks_B
	
		posterior_A=posterior(event, chunk_A, agent_B, oldpssblchnks_B)
		A_report.append(posterior_A)
		newpssblchnks_A=pssblchnks(posterior_A, event, agent_A, agent_B, oldpssblchnks_B, oldpssblchnks_A)

		posterior_B=posterior(event, chunk_B, agent_A, newpssblchnks_A)
		B_report.append(posterior_B)
		newpssblchnks_B=pssblchnks(posterior_B, event, agent_B, agent_A, newpssblchnks_A, oldpssblchnks_B)
	return (A_report,B_report)

#Given agent's current belief,
#initial report, and final report
#Returns expected payoff of report
def payoff(belief,init_rprt,fin_rprt):
	if init_rprt==0:
		init_rprt=0.01
	if init_rprt==1:
		init_rprt=0.99
	if fin_rprt==0:
		fin_rprt=0.01
	if fin_rprt==1:
		fin_rprt=0.99
	payoff=belief*math.log(fin_rprt/init_rprt)+(1-belief)*math.log((1-fin_rprt)/(1-init_rprt))
	return payoff

#Given lists of reported posteriors
#Checks if an agent ever retroactively
#regrets any of their reports
def check_rtrctv_rgrt(reports):
	for i in range(len(reports[0])):
		for j in range(2):
			for k in range(i+1):
				if (k==0 and j==0):
					if payoff(reports[j][i], 1/2, reports[j][k])<0:
						return True
				elif (j==0): 
					if payoff(reports[j][i], reports[j+1][k-1], reports[j][k])<0:
						return True
				elif (j==1):
					if payoff(reports[j][i], reports[j-1][k], reports[j][k])<0:
						return True
	return False
			

world=1
event=[3,6,9]
num_turns=0

while(True):
	agent_A=partition(list(range(1,11)))
	agent_B=partition(list(range(1,11)))
	reports=communicate(world,event,agent_A,agent_B)
	num_turns=len(reports[0])
	if check_rtrctv_rgrt(reports)==True:
		print(num_turns)
		if num_turns>=4:
			break

print(agent_A)
print(agent_B)
print(reports)
