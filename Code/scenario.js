//Given list of worlds
//Generates random info partition
function partition(list) {
    if (list.length == 1) {
        return [list]
    } else {
        var part = partition(list.slice(0, list.length-1))
        var place = Math.floor(Math.random() * (part.length+1))
        if (place == part.length) {
            part.push([list[list.length-1]])
        } else {
            part[place].push(list[list.length-1])
        }
        return part
    }
}

//Given a world and an info partition
//Returns chunk the world is contained in
function which_chunk(world, part) {
    for(chunck of part) {
        if(chunk.includes(world)) {
            return chunk
        }
    }
    return undefined //Error
}

//Given info partition and list of chunk indices
//Returns union of chunks corresponding to indices
function unionchunks(part, chunks) {
	var union = []
	for(i of chunks) {
		union=union.concat(part[i])
    }
	return union
}

function setIntersection(set1, set2) {
    return new Set([...set1].filter(x => set2.has(x)))
}

//Given event, chunk of agent, opponent's info partition, 
//and list of opponent's possible chunks
//Returns posterior of agent
function posterior(event, chunk, opp_part, opp_chnks) {
    var setEvent = new Set(event)
    var setChunk = new Set(chunk)
    var setOppPartChunk = new Set(unionchunks(opp_part, opp_chnks))
    var top = setIntersection(setIntersection(setEvent, setChunk), setOppPartChunk)
    var bottom = setIntersection(setChunk, setOppPartChunk)

    return top.size / bottom.size
}

//Given posterior, event, info partition, opponent's
//info partition, and opponent's possible chunks
//Returns possible chunks consistent 
//with reported posterior
function pssblchnks(post, event, part, opp_part, opp_chunks, oldpssblchnks){
	var chunks = []
	for (let chunk of part) {
        var setChunk = new Set(chunk)
        var setOppPartChunk = new Set(unionchunks(opp_part, opp_chunks))
        var intersect = setIntersection(setChunk, setOppPartChunk)
	var chunk_post = undefined
        if (intersect.size != 0){
            chunk_post = posterior(event, chunk, opp_part, opp_chunks)
        }
	
	if (chunk_post == post){
	    chunks.push(part.indexOf(chunk))
        }
    }
	return new Array(setIntersection(new Set(chunks), new Set(oldpssblchnks)))
}

//Given true state of world, event, and
//both agents' information partitions
//Simulates communication process and returns
//list of reported posteriors for both agents
// function communicate(world, event, agent_A, agent_B){
// 	var chunk_A = which_chunk(world, agent_A)
// 	var chunk_B = which_chunk(world,agent_B)
// 	var oldpssblchnks_A = Array.from(Array(agent_A).keys())
// 	var oldpssblchnks_B = Array.from(Array(agent_B).keys())
// 	var A_report = []
// 	var B_report = []
	
// 	var posterior_A = posterior(event, chunk_A, agent_B, oldpssblchnks_B)
// 	A_report.push(posterior_A)
// 	var newpssblchnks_A = pssblchnks(posterior_A, event, agent_A, agent_B, oldpssblchnks_B, oldpssblchnks_A)
	
// 	posterior_B=posterior(event, chunk_B, agent_A, newpssblchnks_A)
// 	B_report.append(posterior_B)
// 	newpssblchnks_B=pssblchnks(posterior_B, event, agent_B, agent_A, newpssblchnks_A, oldpssblchnks_B)

// 	while (newpssblchnks_A!=oldpssblchnks_A or newpssblchnks_B!=oldpssblchnks_B):
// 		oldpssblchnks_A=newpssblchnks_A
// 		oldpssblchnks_B=newpssblchnks_B
	
// 		posterior_A=posterior(event, chunk_A, agent_B, oldpssblchnks_B)
// 		A_report.append(posterior_A)
// 		newpssblchnks_A=pssblchnks(posterior_A, event, agent_A, agent_B, oldpssblchnks_B, oldpssblchnks_A)

// 		posterior_B=posterior(event, chunk_B, agent_A, newpssblchnks_A)
// 		B_report.append(posterior_B)
// 		newpssblchnks_B=pssblchnks(posterior_B, event, agent_B, agent_A, newpssblchnks_A, oldpssblchnks_B)
// 	return (A_report,B_report)
// }

let worlds = [1,2,3,4,5,6,7,8,9,10]
let worldView = partition(worlds)
console.log(worldView)

let evnt = [3,6,9]
let myView=[[1,3,6,7,8],[2,4,5,9,10]]
let oldpssbl=Array.from(Array(myView.length).keys())
console.log(myView)
console.log(oldpssbl)
let chunk=[1,3,6,7,8]
let oppchunks=[0,1]
let post=posterior(evnt,chunk,worldView,oppchunks)
console.log(post)
console.log(pssblchnks(post,evnt,myView,worldView,oppchunks,oldpssbl))
