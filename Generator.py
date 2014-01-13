import networkx
import sys
import random

class Generator:

    def __generate_euler_graph(self, node_number, edge_number, h_or_f):
        isOk = self.checkNumbers(node_number, edge_number, h_or_f)
        if isOk is False:
            return None

        if h_or_f == 'FULL':
            edge_number -= 1

        G = networkx.Graph()
        random.seed()
        is_parity = node_number % 2 == 0

        vailable_nodes = self.__prepare_vailable_nodes_array(node_number)
        is_visited_array = self.__prepare_is_visited_array(node_number)

        begin_node = self.__rand_begin_node(node_number)

        last_node = begin_node

        unvisited_nodes_number = node_number
        unvisited_nodes_number = self.__node_is_visited(begin_node,
                                                is_visited_array,
                                                unvisited_nodes_number)

        while(unvisited_nodes_number < edge_number):
            actual_index = random.randint(0, len(vailable_nodes[last_node]) - 1)

            actual_node = vailable_nodes[last_node][actual_index]
            G.add_edge(last_node, actual_node)

            vailable_nodes[last_node].pop(actual_index)
            vailable_nodes[actual_node].remove(last_node)

            if is_parity:
                if len(vailable_nodes[last_node]) == 1:
                    node = vailable_nodes[last_node].pop()
                    vailable_nodes[node].remove(last_node)

            last_node = actual_node
            edge_number -= 1

            unvisited_nodes_number = self.__node_is_visited(last_node,
                                                    is_visited_array,
                                                    unvisited_nodes_number)

        nodes_rest = []
        for i in range(len(is_visited_array)):
            if is_visited_array[i] is False:
                nodes_rest.append(i)
        if len(nodes_rest) != edge_number:
            print "Error size\n" + "nodes_rest: " + str(nodes_rest) + \
                "\nedge_number: " + str(edge_number)

        while(edge_number > 0):
            if len(nodes_rest) == 1:
                index = 0
            else:
                index = random.randint(0, len(nodes_rest) - 1)

            actual_node = nodes_rest[index]
            G.add_edge(last_node, actual_node)
            #print str(last_node) + " " + str(actual_node)

            last_node = actual_node
            edge_number -= 1

            nodes_rest.pop(index)

        if h_or_f == 'FULL':
           G.add_edge(last_node, begin_node)
        return G

    def checkNumbers(self, node_number, edge_number, h_or_f):
        if node_number == 0:
            print "node number:" + str(node_number)
            return False

        if h_or_f == 'FULL':
            if node_number <= 3:
                print "node number:" + str(node_number)
                return False

        edge_max = 0
        if node_number %2 == 0:
            edge_max = (node_number*(node_number - 2))/2
            if h_or_f == 'HALF':
                edge_max += 1
        else:
            edge_max = (node_number*(node_number - 1))/2

        edge_min = 0
        if h_or_f == 'FULL':
            edge_min = node_number
        elif h_or_f == 'HALF':
            edge_min = node_number - 1

        if edge_number >= edge_min and edge_number <= edge_max:
            return True
        else:
            print "edge_number: "+ str(edge_number) + "\n"
            print "edge_min: "+ str(edge_min) + "\n"
            print "edge_max: "+ str(edge_max) + "\n"
            print "node_number: "+ str(node_number) + "\n"
            return False

    def generate_half_euler_graph(self, node_number, edge_number):
        return self.__generate_euler_graph(node_number, edge_number, 'HALF')


    def generate_full_euler_graph(self, node_number, edge_number):
        return self.__generate_euler_graph(node_number, edge_number, 'FULL')

    def __prepare_vailable_nodes_array(self, node_number):
        vailable_nodes = [[] for i in range(node_number)]
        for i in range(node_number):
            for j in range(node_number - 1):
                if j >= i:
                    vailable_nodes[i].append(j + 1)
                else:
                    vailable_nodes[i].append(j)
        return vailable_nodes


    def __prepare_is_visited_array(self,node_number):
        is_visited = []
        for i in range(node_number):
            is_visited.append(False)

        return is_visited


    def __node_is_visited(self, index, array, unvisited_number):
        if array[index] is False:
            array[index] = True
            unvisited_number -= 1
        return unvisited_number


    def __rand_begin_node(self, node_number):
        return random.randint(0, node_number - 1)



