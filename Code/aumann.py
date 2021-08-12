import random
import math

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

def which_chunk(world, part):
	for chunk in part:
		if world in chunk:
			return chunk

def unionchnks(part,chnks):
	union=[]
	for i in chnks:
		union+=part[i]
	return union

def pssblchnks(posterior, event, part, opp_part, opp_chnks):
	chnks=[]
	for chunk in part:
		if len(set(chunk) & set(unionchnks(opp_part, opp_chnks)))!=0:
			chunk_post=len(set(event) & (set(chunk) & set(unionchnks(opp_part, opp_chnks))))/len(set(chunk) & set(unionchnks(opp_part, opp_chnks)))
		else:
			chunk_post="Undefined"
		if chunk_post==posterior:
			chnks.append(part.index(chunk))
	return chnks

def communicate(world, event, agent_A, agent_B):
	chunk_A=which_chunk(world,agent_A)
	chunk_B=which_chunk(world,agent_B)
	oldpssblchnks_A=range(len(agent_A))
	oldpssblchnks_B=range(len(agent_B))
	A_report=[]
	B_report=[]

	posterior_A=len(set(event) & (set(chunk_A) & set(unionchnks(agent_B, oldpssblchnks_B))))/len(set(chunk_A) & set(unionchnks(agent_B, oldpssblchnks_B)))
	A_report.append(posterior_A)
	newpssblchnks_A=pssblchnks(posterior_A, event, agent_A, agent_B, oldpssblchnks_B)

	posterior_B=len(set(event) & (set(chunk_B) & set(unionchnks(agent_A, newpssblchnks_A))))/len(set(chunk_B) & set(unionchnks(agent_A, newpssblchnks_A)))
	B_report.append(posterior_B)
	newpssblchnks_B=pssblchnks(posterior_B, event, agent_B, agent_A, newpssblchnks_A)

	while (newpssblchnks_A!=oldpssblchnks_A or newpssblchnks_B!=oldpssblchnks_B):
		oldpssblchnks_A=newpssblchnks_A
		oldpssblchnks_B=newpssblchnks_B
	
		posterior_A=len(set(event) & (set(chunk_A) & set(unionchnks(agent_B, oldpssblchnks_B))))/len(set(chunk_A) & set(unionchnks(agent_B, oldpssblchnks_B)))
		A_report.append(posterior_A)
		newpssblchnks_A=pssblchnks(posterior_A, event, agent_A, agent_B, oldpssblchnks_B)

		posterior_B=len(set(event) & (set(chunk_B) & set(unionchnks(agent_A, newpssblchnks_A))))/len(set(chunk_B) & set(unionchnks(agent_A, newpssblchnks_A)))
		B_report.append(posterior_B)
		newpssblchnks_B=pssblchnks(posterior_B, event, agent_B, agent_A, newpssblchnks_A)
	return (A_report,B_report)

def check_rtrctv_rgrt(report):
	Report=[1/2]+report
	for i in range(1,len(Report)):
		for j in range(i):
			if Report[j]==0:
				Report[j]=0.01
			if Report[j+1]==0:
				Report[j+1]=0.01
			if Report[j]==1:
				Report[j]=0.99
			if Report[j+1]==1:
				Report[j+1]=0.99
			payoff=Report[i]*math.log(Report[j+1]/Report[j])+(1-Report[i])*math.log((1-Report[j+1])/(1-Report[j]))
			if payoff<0:
				return True
	return False
			

world=1
event=[5,10,15,20]

rtrctv_rgrt=False
while(rtrctv_rgrt==False):
	agent_A=partition(list(range(1,26)))
	agent_B=partition(list(range(1,26)))
	reports=communicate(world,event,agent_A,agent_B)
	if (check_rtrctv_rgrt(reports[0])==True or check_rtrctv_rgrt(reports[1])==True):
		rtrctv_rgrt=True

print(agent_A)
print(agent_B)
print(reports)
