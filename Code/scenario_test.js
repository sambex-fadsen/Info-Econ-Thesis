var __spreadArray = (this && this.__spreadArray) || function (to, from) {
    for (var i = 0, il = from.length, j = to.length; i < il; i++, j++)
        to[j] = from[i];
    return to;
};
//Given list of worlds
//Generates random info partition
function partition(list) {
    if (list.length == 1) {
        return [list];
    }
    else {
        var part = partition(list.slice(0, list.length - 1));
        var place = Math.floor(Math.random() * (part.length + 1));
        if (place == part.length) {
            part.push([list[list.length - 1]]);
        }
        else {
            part[place].push(list[list.length - 1]);
        }
        return part;
    }
}
//Given a world and an info partition
//Returns chunk the world is contained in
function which_chunk(world, part) {
    for (var _i = 0, part_1 = part; _i < part_1.length; _i++) {
        var chunk_1 = part_1[_i];
        if (chunk_1.indexOf(world) != -1) {
            return chunk_1;
        }
    }
    return undefined; //Error
}
//Given info partition and list of chunk indices
//Returns union of chunks corresponding to indices
function unionchunks(part, chunks) {
    var union = [];
    for (var _i = 0, chunks_1 = chunks; _i < chunks_1.length; _i++) {
        var i = chunks_1[_i];
        union = union.concat(part[i]);
    }
    return union;
}
function setIntersection(set1, set2) {
    return new Set(__spreadArray([], set1).filter(function (x) { return set2.has(x); }));
}
//Given event, chunk of agent, opponent's info partition, 
//and list of opponent's possible chunks
//Returns posterior of agent
function posterior(event, chunk, opp_part, opp_chnks) {
    var setEvent = new Set(event);
    var setChunk = new Set(chunk);
    var setOppPartChunk = new Set(unionchunks(opp_part, opp_chnks));
    var top = setIntersection(setIntersection(setEvent, setChunk), setOppPartChunk);
    var bottom = setIntersection(setChunk, setOppPartChunk);
    return top.size / bottom.size;
}
var worlds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
var worldView = partition(worlds);
console.log(worldView);
var evnt = [3, 6, 9];
var chunk = [1, 3, 6, 7, 8];
var oppchunks = [0, 1];
console.log(posterior(evnt, chunk, worldView, oppchunks));
