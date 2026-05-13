

def predecessore(graph, successore):
    pred = []
    for nodo in graph:
        #print(graph[nodo])
        if successore in graph[nodo]:
            pred.append(nodo) 
    return pred

def instanziaTabella(pattern, graph):
    print("ciao")

def ordinaTopo(graph, head):
    visitati = set()
    topoList = []

    topoList.append(head)

    def dfs(nodo):
        if nodo in visitati:
            return
        else:
            visitati.add(nodo)
            for children in graph[nodo]:
                if children not in topoList:
                    topoList.append(children)
            for children in graph[nodo]:
                try:
                    dfs(children)
                except:
                    print("end of the line :3")
    dfs(head)
    return topoList




    

def main():
    graph = {
        "1" : ["2","3"],
        "2" : ["4"],
        "3" : ["4"]
    }
    etichette={
        "1":["C"],
        "2":["A"],
        "3":["T"],
        "4":["C"]
    }

    pattern = "CAC"
    
    print(ordinaTopo(graph, "1"))



print("hello")
main()


