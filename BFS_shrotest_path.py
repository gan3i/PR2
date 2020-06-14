from queue import Queue
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

def bfs_new(start,end):
    visited = []
    q = [[start]]
    if start == end:
        return "do not searhc for home from home"
    #q.put([start])
    # q.put([start])
    while q:
        path = q.pop(-1)
        current = path[-1]
        for nhbr in adj_list[current]:
            if nhbr not in visited:
                new_path = path + [nhbr]
                q.append(new_path)
                if nhbr == end:
                    return new_path
        visited.append(current)
    return "no path"

print(bfs_new(10,15))




























# def bfs(start,end):
#     if start == end:
#         return "That was easy! Start = goal"
#     visited = []
#     q = [[start]]
#     while q:
#         path = q.pop(0)       
#         current = path[-1]
#         if current not in visited:           
#             nhbrs = adj_list[current]
#             for nbr in nhbrs:
#                 new_path = list(path)
#                 new_path.append(nbr)
#                 q.append(new_path)
#                 if nbr == end:
#                     return new_path
#             visited.append(current)
#     return "No Path"

# print(bfs(10,1))

