import sys
import numpy as np

def check_core_point(point, points):
    Eps = int(sys.argv[3])
    x_coordinate = float(point[1])
    y_coordinate = float(point[2])
    neighbor = list()
    for obj in range(len(points)):
        obj_x = float(points[obj][1])
        obj_y = float(points[obj][2])
        distance = np.sqrt(np.power(x_coordinate-obj_x, 2)+np.power(y_coordinate-obj_y, 2))
        if distance <= Eps: neighbor.append(points[obj])
    return neighbor

def DBSCAN(points):
    count = 0
    cluster = list()
    MinPts = int(sys.argv[4])
    visited = [False] * len(points)
    for point in points:
        if visited[int(point[0])]==True: continue
        neighbor = check_core_point(point, points)
        if len(neighbor)>=MinPts: 
            cluster.append(list())
            while True:
                if len(neighbor)==0: break
                next_point = neighbor.pop()
                if visited[int(next_point[0])]==True: continue
                visited[int(next_point[0])]=True
                cluster[count].append(next_point[0])
                new_neighbors = check_core_point(next_point, points)
                if len(new_neighbors)>=MinPts:neighbor+=new_neighbors
            count += 1
        else: visited[int(point[0])]=True
    cluster.sort(key=len, reverse=True)
    cluster = [sorted(list(set(list(map(int, l))))) for l in cluster]
    return cluster

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()
        points = [list(line.strip().split('\t')) for line in lines]
    cluster = DBSCAN(points)
    output = sys.argv[1].split('/')[2].split('.')[0]
    for i in range(int(sys.argv[2])):
        with open('./test-2/'+output+'_cluster_'+str(i)+'.txt', 'w') as f:
            for obj in cluster[i]:
                f.write(str(obj)+'\n')
