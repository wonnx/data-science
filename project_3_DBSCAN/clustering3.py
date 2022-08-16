import sys, math
global visit, isCore, cluster, neighbor
sys.setrecursionlimit(15000)
def visit_and_cluster(core):
    global visit, isCore, cluster, neighbor
    #print(isCore[int(core)])
    if isCore[int(core)]:
        if visit[int(core)] == False:  # 방문했다면 그냥 패스
            visit[int(core)] = True
            cluster.append(core)

            #print(N_list[int(core)])
            for n in neighbor[int(core)]:
                #print(n)
                if visit[int(n)] == False:
                    cluster.append(n)
                    visit_and_cluster(n)
    else:
        return

if __name__ == "__main__":
    global isCore, visit, cluster, neighbor
    print(sys.getrecursionlimit())
    file = open(sys.argv[1], "r") #input 파일
    objects = list() #list 만들기

    isCore = None
    CoreList = list()

    while True: #input 파일 읽어서 쪼개기
        line = file.readline().strip()
        if not line:
            break
        objects.append(line.split('\t'))
    
    visit = [False] * len(objects) #처음에 모두 false
    isCore = [False] * len(objects)
    Eps = int(sys.argv[3])
    MinPts = int(sys.argv[4])

    cluster = list() #클러스터 리스트 만들기
    cluster_list = list()
    c_idx = 0 #index 0부터 시작
    N_list = list()
    neighbor = list()  # neighber list 만들기
    ###########################################
    for idx in range(len(objects)): #object 돌면서 방문했으면 continue,
        #print(int(objects[idx][0]))
        if visit[int(objects[idx][0])] == True:
            continue
        n_neighbor = list()
        x = float(objects[idx][1])
        y = float(objects[idx][2])

        for p in objects: #거리 구하고 거리가 eps 이하라서 범위 안에 있다면 object 이웃으로 넣기
            dist = math.sqrt(math.pow(x-float(p[1]), 2)
                            +math.pow(y-float(p[2]), 2))
            if dist <= Eps:
                n_neighbor.append(p[0])

        if len(n_neighbor) >= MinPts: #네이버의 수가 MinPts 이상이면
            isCore[idx] = True
            CoreList.append(idx)
            neighbor.append(n_neighbor)
        else:
            neighbor.append(list())

    for core in CoreList:
        #print(core)
        cluster = list()
        visit_and_cluster(core)

        if(len(cluster)) > 0:
            cluster_list.append(cluster)






        #     n_idx = 0 #neighber index 0부터 시작
        #     cluster.append(list()) #클러스터에 리스트로 넣어주고
        #     while n_idx < len(neighbor):
        #         neighbor_obj = neighbor[n_idx] #인덱스에 해당하는 이웃 obj을 neighbor_obj
        #         n_idx += 1 #하나 증가시키고
        #         if visit[int(neighbor_obj[0])] == True: #방문했다면 그냥 패스
        #             continue
        #
        #         visit[int(neighbor_obj[0])] = True #아니라면 방문했다고 만들기
        #         cluster[c_idx].append(neighbor_obj[0]) #클러스터에 넣어버리기
        #
        #         new_neighbors = list() #새로운 이웃 리스트 만들기
        #
        #         x_ = float(neighbor_obj[1])
        #         y_ = float(neighbor_obj[2])
        #         for  new_obj in objects: #다시 거리 비교
        #             dist = math.sqrt(math.pow(x_-float(new_obj[1]), 2)
        #                             +math.pow(y_-float(new_obj[2]), 2))
        #             if dist <= Eps:
        #                 new_neighbors.append(new_obj)
        #
        #         if len(new_neighbors) >= MinPts:
        #             neighbor += new_neighbors
        #     c_idx += 1
        # else:
        #     visit[int(obj[0])] = True

    cluster_idx = 0
    output = list()
    for cluster_list_item in cluster_list:
        output.append((len(cluster_list_item), cluster_idx))
        cluster_idx += 1

    output.sort(key=len, reverse=True)

    for i in range(int(sys.argv[2])):
        route = sys.argv[1][9:15] + '_cluster_'
        route += str(i) + '.txt'
        index = output[i][1]
        with open(route, 'w') as f:
            for obj in cluster_list[index]:
                f.write(str(obj) + '\n')

    f.close()
    file.close()