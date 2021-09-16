
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

console.log(partition([1,2,3,4,5,6,7,8]))
