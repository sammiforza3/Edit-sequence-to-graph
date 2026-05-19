

def predecessore(graph, successore):
    pred = []
    for nodo in graph:
        #print(graph[nodo])
        if successore in graph[nodo]:
            pred.append(nodo) 
    if pred == []:
        return "0"
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
                    print("")
    dfs(head)
    return topoList

def emptyMatrix(righe, colonne):
    matrix = []

    for i in range(0,righe):
        riga = []
        for j in range(0,colonne):
            riga.append(0)
        matrix.append(riga)

    return matrix;



    

def calcolateMove(matrix, riga, colonna, graph, node, topolist):
    #troviamo il predecessore con costo minore
    pred = predecessore(graph, node)

    #match 
    #troviamo il predecessore che pesa meno SULLA MATRICE alla riga precedente
    celle = []
    for i in range (0, colonna):
        if topolist[i] in pred:
            celle.append(matrix[riga-1][i])
    match = min(celle)

    #insert
    insert = matrix[riga-1][colonna]

    #delete
    celle = []
    for i in range (0, colonna):
        if topolist[i] in pred:
            celle.append(matrix[riga][i])
    delete = min(celle)

    return min([match, insert, delete])




    

#function that buils the dynamic programming matrix
def buildMatrix(graph, etichette, head, pattern, weight):
    topoList = ordinaTopo(graph, head)
    pattern = "e" + pattern
    righe = len(pattern)
    colonne = len(topoList)
    matrix = emptyMatrix(righe, colonne)
    cost = -1000;
    #nota: mat[0,0] = 0
    for i in range(0, righe):
        matrix[i][0] = i * weight #gestione verticale inserimento pattern


    for c in range(1,colonne):
        #trova il minimo predecessore del nodo
        nodes = predecessore(graph,topoList[c])
        cellsPreds=[]
        for i in range(0,c):
            if(topoList[i] in nodes):
                candidate = matrix[0][i]
                cellsPreds.append(candidate)
        matrix[0][c] = min(cellsPreds) + weight

    for i in range(1, righe):
        for c in range(1, colonne):
            #matrix[i,c] = computeCell(matrix,righe, colonne, graph, head, pattern, 4)
            if pattern[i] == etichette[topoList[c]][0]:
                #match
                if(pattern[i] == 'A'):
                    cost = 0
                else:
                    cost = 1
            else:
                cost = weight;
            matrix[i][c] = calcolateMove(matrix, i, c, graph, topoList[c],topoList) + cost

    return matrix

    


def fixGraph(graph, head, etichette):
    topolist = ordinaTopo(graph, head)
    graph.update({"0":[topolist[0]]})
    etichette.update({"0":["S0"]})
    

def main():
    graph = {
        "1" : ["2","3"],
        "2" : ["4"],
        "3" : ["4"],
        "4" : []
    }
    etichette={
        "1":["C"],
        "2":["A"],
        "3":["T"],
        "4":["C"]
    }

    pattern = "CAC"
    
    fixGraph(graph, "1", etichette)
    print(graph)
    print(ordinaTopo(graph, "0"))
    print(buildMatrix(graph, etichette, "0", pattern, 4))


#RICORDAESI DI METTERE IL PREDECESSORE
print("hello")
main()


