from queue import LifoQueue

adj_list = {10:[6,7,8,14,13,9],
            6:[10,13,7],
            7:[10,6,8],
            8:[10,7,9],
            9:[10,8,15,14],
            14:[10,13,9,16],
            13:[10,5,6,14],
            15:[16,9],
            16:[17,15,14],
            17:[12,16],
            12:[5,18,17],
            5:[3,4,11,12,13],
            3:[5,2],
            2:[3,1],
            1:[2],
            11:[5,4,18],
            4:[11,5],
            18:[11,12]}
def dfs(start,end):
    visited = []
    q = LifoQueue() # can be implemented with list or collection.deque as well
    q.put([start])
    while q:
        path = q.get()
        current = path[-1]
        for nhbr in adj_list[current]:
            if nhbr not in visited:
                new_path = path +[nhbr]
                q.put(new_path)
                if nhbr == end :
                    return new_path
        visited.append(current)

print(dfs(10,15))









