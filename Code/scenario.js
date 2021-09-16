
function partition(list) {
    if (list.length == 1) {
        return [list]
    } else {
        var part = partition(list.slice(0, list.length-1))
        var place = Math.floor(Math.random() * part.length+1)
        if (place == part.length) {
            part.push([list[list.length-1]])
        } else {
            part[place].push(list[list.length-1])
        }
        return part
    }
}

function partition_ALT(list) {
    var shuffled = list.sort((a, b) => 0.5 - Math.random())
    var output = []
    var temp = []

    while(shuffled.length > 1) {
        var numPop = Math.floor(Math.random() * shuffled.length) + 1
        
        for(var i = 0; i < numPop; i++) {
            temp.push(shuffled.pop())
        }
        output.push(temp)
        temp = []
    }
    return output
}

//console.log(partition([1,2,3,4,5,6,7,8]))
console.log(partition_ALT([1,2,3,4,5,6,7,8]))