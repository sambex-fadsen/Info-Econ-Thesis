//Given list of worlds
//Generates random info partition
function partition(list: number[]):number[][] {
    if (list.length == 1) {
        return [list]
    } else {
        let part = partition(list.slice(0, list.length-1))
        let place = Math.floor(Math.random() * (part.length+1))
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
function which_chunk(world:number, part:number[][]):number[] {
    for(let chunk of part) {
        if(chunk.indexOf(world) != -1) {
            return chunk
        }
    }
    return undefined //Error
}

//Given info partition and list of chunk indices
//Returns union of chunks corresponding to indices
function unionchunks(part:number[][], chunks:number[]):number[] {
	let union:number[] = []
	for(let i of chunks) {
        union = union.concat(part[i])
    }
	return union
}

function setIntersection(set1: Set<number>, set2: Set<number>) {
    return new Set([...set1].filter(x => set2.has(x)))
}

//Given event, chunk of agent, opponent's info partition, 
//and list of opponent's possible chunks
//Returns posterior of agent
function posterior(event:number[], chunk:number[], opp_part:number[][], opp_chnks: number[]) {
    var setEvent = new Set(event)
    var setChunk = new Set(chunk)
    var setOppPartChunk = new Set(unionchunks(opp_part, opp_chnks))
    
    var top = setIntersection(setIntersection(setEvent, setChunk), setOppPartChunk)
    var bottom = setIntersection(setChunk, setOppPartChunk)

    return top.size / bottom.size
}

let worlds = [1,2,3,4,5,6,7,8,9,10]
let worldView = partition(worlds)
console.log(worldView)

let evnt = [3,6,9]
let chunk=[1,3,6,7,8]
let oppchunks=[0,1]
console.log(posterior(evnt, chunk, worldView, oppchunks))

