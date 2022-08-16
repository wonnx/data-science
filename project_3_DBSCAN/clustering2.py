import sys, math

if __name__ == "__main__":
    file = open(sys.argv[1], "r")
    n = int(sys.argv[2])
    Eps = int(sys.argv[3])
    MinPts = int(sys.argv[4])

    objects = list()
    while True:
        line = file.readline().strip()
        if not line:
            break
        objects.append(line.split('\t'))

    c_idx = 0
    cluster = list()
    visit = [False] * len(objects)

    for obj in objects:
        if visit[int(obj[0])] == True:
            continue

        neighbor = list()
        for o in objects:
            dist = math.sqrt(math.pow((float(obj[1])-float(o[1])), 2)
                             + math.pow((float(obj[2])-float(o[2])), 2))
            if dist <= Eps:
                neighbor.append(o)

        if len(neighbor) >= MinPts:
            n_idx = 0
            cluster.append(list())
            while True:
                if n_idx >= len(neighbor):
                    break
                point = neighbor[n_idx]
                n_idx += 1
                if visit[int(point[0])] == True:
                    continue
                visit[int(point[0])] = True
                cluster[c_idx].append(point[0])

                new_neighbors = list()
                for o in objects:
                    dist = math.sqrt(math.pow((float(point[1])-float(o[1])), 2)
                              + math.pow((float(point[2])-float(o[2])), 2))
                    if dist <= Eps:
                        new_neighbors.append(o)

                if len(new_neighbors) >= MinPts:
                    neighbor += new_neighbors
            c_idx += 1
        else:
            visit[int(obj[0])] = True

    cluster.sort(key=len, reverse=True)

    output = list()
    for c in cluster:
        output.append(sorted(list(map(int, c))))

    for i in range(n):
        route = sys.argv[1][:6] + '_cluster_'
        route += str(i) + '.txt'
        with open(route, 'w') as f:
            for obj in output[i]:
                f.write(str(obj)+'\n')