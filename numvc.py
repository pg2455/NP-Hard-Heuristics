import os, random
import numpy as np
import networkx as nx

current_dir = os.path.dirname(os.path.realpath(__file__))
numvc_cmd = os.path.join(current_dir, "NuMVC/numvc")
output_dir = os.path.join(current_dir, "NuMVC/output/")
input_dir = os.path.join(current_dir, "NuMVC/input/")

def ls_mvc(input_file, output_file, cutoff_time):
    cmd = "{} {} 0 1 {} > {}".format(numvc_cmd, input_file, cutoff_time, output_file)
    os.system(cmd)


def get_numvc(graph, cutoff_time):
    # time is in seconds
    _id = random.randint(0,1000)
    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()
    input_file = os.path.join(input_dir,"{}.txt".format(_id))
    output_file = os.path.join(output_dir, "{}.txt".format(_id))

    with open(input_file,"w") as f:
        f.write("p edge {} {}\n".format(nodes, edges))
        for u,v in graph.edges:
            f.write("e {} {}\n".format(u+1, v+1))

    ls_mvc(input_file, output_file, cutoff_time)

    with open(output_file) as f:
        vc_size = int(f.readlines()[2].split("=")[-1].strip())


    with open(output_file) as f:
        IS =  map(lambda x: int(x) - 1, f.readlines()[5].split())

    vc = {u for u in range(nodes) if u not in IS}
    return vc


if __name__ == "__main__":
    graph = nx.barabasi_albert_graph(n=200,m=2)
    print "graph nodes:{} edges:{}".format(graph.number_of_nodes(), graph.number_of_edges())

    vc = get_numvc(graph, 1)
    print "numvc output - vc size: {}".format(len(vc))
