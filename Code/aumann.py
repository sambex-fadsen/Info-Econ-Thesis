import random

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
	A_reports=[]
	B_reports=[]

	posterior_A=len(set(event) & (set(chunk_A) & set(unionchnks(agent_B, oldpssblchnks_B))))/len(set(chunk_A) & set(unionchnks(agent_B, oldpssblchnks_B)))
	A_reports.append(posterior_A)
	newpssblchnks_A=pssblchnks(posterior_A, event, agent_A, agent_B, oldpssblchnks_B)

	posterior_B=len(set(event) & (set(chunk_B) & set(unionchnks(agent_A, newpssblchnks_A))))/len(set(chunk_B) & set(unionchnks(agent_A, newpssblchnks_A)))
	B_reports.append(posterior_B)
	newpssblchnks_B=pssblchnks(posterior_B, event, agent_B, agent_A, newpssblchnks_A)

	while (newpssblchnks_A!=oldpssblchnks_A or newpssblchnks_B!=oldpssblchnks_B):
		oldpssblchnks_A=newpssblchnks_A
		oldpssblchnks_B=newpssblchnks_B
	
		posterior_A=len(set(event) & (set(chunk_A) & set(unionchnks(agent_B, oldpssblchnks_B))))/len(set(chunk_A) & set(unionchnks(agent_B, oldpssblchnks_B)))
		A_reports.append(posterior_A)
		newpssblchnks_A=pssblchnks(posterior_A, event, agent_A, agent_B, oldpssblchnks_B)

		posterior_B=len(set(event) & (set(chunk_B) & set(unionchnks(agent_A, newpssblchnks_A))))/len(set(chunk_B) & set(unionchnks(agent_A, newpssblchnks_A)))
		B_reports.append(posterior_B)
		newpssblchnks_B=pssblchnks(posterior_B, event, agent_B, agent_A, newpssblchnks_A)
	return (A_reports,B_reports)

world=1
event=[1,5,9]
agent_A=[[1,2,3],[4,5,6],[7,8,9]]
agent_B=[[1,2,3,4],[5,6,7,8],[9]]

reports=communicate(world,event,agent_A,agent_B)

print(agent_A)
print(agent_B)
print(reports)
