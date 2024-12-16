import random
from collections import deque
import time

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0] * vertices for i in range(vertices)]

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity

    def bfs(self, source, sink, parent):
        visited = [False] * self.V
        queue = deque()
        queue.append(source)
        visited[source] = True

        while queue:
            u = queue.popleft()
            for v in range(self.V):
                if not visited[v] and self.graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    def edmonds_karp(self, source, sink):
        start_time = time.time()
        parent = [-1] * self.V
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
        end_time = time.time()
        print(f"Время выполнения алгоритма {end_time - start_time} с")
        return max_flow


def generate_random_graph(vertices, density=0.3, min_capacity=1, max_capacity=10, allow_fractions=False):
    graph = Graph(vertices)
    for u in range(vertices):
        for v in range(vertices):
            if u != v and random.random() < density:
                if allow_fractions:
                    capacity = random.uniform(min_capacity, max_capacity)
                else:
                    capacity = random.randint(min_capacity, max_capacity)
                graph.add_edge(u, v, capacity)
    return graph


def test_edmonds_karp(vertices, density=0.3, allow_fractions=False):
    graph = generate_random_graph(vertices, density, allow_fractions=allow_fractions)
    source = 0
    sink = vertices - 1
    max_flow = graph.edmonds_karp(source, sink)
    print(f"Vertices: {vertices}, Max Flow: {max_flow}")


def main():
    while True:
        print("Выберите тестирование (введите 1, 2 или 3)\n1. Небольшой граф (6 вершин) для проверки работы алгоритма\n"
          "2. 10 тестов с графами с различным количеством вершин от 50 до 500, с целыми значениями пропускной способности\n"
          "3. 10 тестов с графами с различным количеством вершин от 50 до 500, с дробными значениями пропускной способности\n"
          "4. 10 тестов с графами с различным количеством вершин от 50 до 500, на плотном графе")
        test_num = input()
        if test_num == '1':
            g = generate_random_graph(6)
            print(*g.graph, sep='\n')
            max_flow = g.edmonds_karp(0, g.V-1)
            print(f"Vertices: {g.V}, Max Flow: {max_flow}")
        elif test_num == '2':
            for i in range(50, 501, 50):
                test_edmonds_karp(i)
        elif test_num == '3':
            for i in range(50, 501, 50):
                test_edmonds_karp(i, 0.3, True)
        elif test_num == '4':
            for i in range(50, 501, 50):
                test_edmonds_karp(i, 0.6)
        else:
            print('Некорректный ввод')
            continue
        break


if __name__ == "__main__":
    main()
