import networkx as nx
import matplotlib.pyplot as plt

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

    def dfs(node):
        if node in visitati:
            return
        
        visitati.add(node)
        
        for child in graph.get(node, []):
            dfs(child)
            
        
        topoList.append(node)

    dfs(head)
    
    return topoList[::-1]

    

def emptyMatrix(righe, colonne):
    matrix = []

    for i in range(0,righe):
        riga = []
        for j in range(0,colonne):
            riga.append(0)
        matrix.append(riga)

    return matrix;



    

def calcolateMove(matrix, riga, colonna, graph, node, topolist, etichette, pattern, weight):
    #troviamo il predecessore con costo minore
    pred = predecessore(graph, node)

    #match 
    #troviamo il predecessore che pesa meno SULLA MATRICE alla riga precedente
    celle = []
    for i in range (0, colonna):
        if topolist[i] in pred:
            celle.append(matrix[riga-1][i])
    
    costo = weight
    if(pattern[riga] == etichette[topolist[colonna]][0]):
        if(pattern[riga] == 'A'):
            costo = 0
        else:
            costo = 1
    match = min(celle) + costo
    

    #insert
    insert = matrix[riga-1][colonna] + weight

    #delete
    celle = []
    for i in range (0, colonna):
        if topolist[i] in pred:
            celle.append(matrix[riga][i])
    delete = min(celle) + weight

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
            move= calcolateMove(matrix, i, c, graph, topoList[c],topoList, etichette, pattern, weight)
            matrix[i][c] = move
    return matrix

def backtracking(matrix, graph, topolist, pattern, etichette, weight=4):
    
    
    
    r = len(pattern) - 1
    c = len(topolist) - 1
    
    percorso_ottimo = []
    
    
    while r > 0 or c > 0:
        valore_corrente = matrix[r][c]
        nodo_corrente = topolist[c]
        mossa_effettuata = False
        
        pred = predecessore(graph, nodo_corrente)
        
        # sostituzione
        if r > 0 and c > 0:
            lettera_pattern = pattern[r]
            lettera_nodo = etichette[nodo_corrente][0]
            
            # Calcoliamo il costo locale
            if lettera_pattern == lettera_nodo:
                costo_diag = 0 if lettera_pattern == 'A' else 1
            else:
                costo_diag = 4
                
            
            for p in pred:
                if p in topolist:
                    idx_p = topolist.index(p)
                    if matrix[r-1][idx_p] + costo_diag == valore_corrente:
                        percorso_ottimo.append(nodo_corrente)
                        r -= 1
                        c = idx_p
                        mossa_effettuata = True
                        break # Usciamo dal ciclo dei predecessori
        
        if mossa_effettuata:
            continue
            
        # Inserzione
        if r > 0:
            if matrix[r-1][c] + weight == valore_corrente:
                r -= 1
                mossa_effettuata = True
                continue
                
        # delezione
        if c > 0 and not mossa_effettuata:
            for p in pred:
                if p in topolist:
                    idx_p = topolist.index(p)
                    if matrix[r][idx_p] + weight == valore_corrente:
                        percorso_ottimo.append(nodo_corrente)
                        c = idx_p
                        mossa_effettuata = True
                        break
                        
       
        if not mossa_effettuata:
            print(f"Errore: Nessun percorso valido trovato dalla cella [{r}][{c}]!")
            break

    # flipping del percoso
    return percorso_ottimo[::-1]
        
    




def fixGraph(graph, head, etichette):
    topolist = ordinaTopo(graph, head)
    graph.update({"0":[topolist[0]]})
    etichette.update({"0":["S0"]})

def calculateEditDistance(graph, etichette, pattern):
    fixGraph(graph, "1", etichette)
    matrix = buildMatrix(graph, etichette, "0", pattern, 4)
    print(matrix)
    return matrix


def printMatrix(matrix, topolist, pattern, etichette):
    # 1. Stampa i nomi dei nodi (Riga 1)
    intestazione_nodi = "      " + " ".join(f"{nodo:>4}" for nodo in topolist)
    print(intestazione_nodi)
    
    # 2. Stampa le etichette dei nodi (Riga 2)
    # Usiamo [0] perché nel tuo dizionario i valori sono liste (es. ["C"])
    intestazione_etichette = "      " + " ".join(f"{etichette[nodo][0]:>4}" for nodo in topolist)
    print(intestazione_etichette)
    
    print("-" * len(intestazione_nodi)) # Riga separatrice
    
    # 3. Aggiunge il gap iniziale al pattern
    pattern_completo = "e" + pattern 
    
    # 4. Stampa ogni riga con la sua lettera corrispondente
    for i, row in enumerate(matrix):
        lettera = pattern_completo[i]
        riga_formattata = " ".join(f"{str(item):>4}" for item in row)
        print(f"{lettera}  | {riga_formattata}")



def plot_grafo(graph, etichette):
    # 1. Creiamo un grafo orientato (Directed Graph)
    G = nx.DiGraph()
    
    # 2. Aggiungiamo tutti i nodi e ci salviamo dentro l'etichetta personalizzata
    for nodo, valore in etichette.items():
        lettera = valore[0]
        # Creiamo un'etichetta tipo "1\n(C)" per andare a capo
        label_personalizzata = f"{nodo}\n({lettera})"
        G.add_node(nodo, label=label_personalizzata)
        
    # 3. Aggiungiamo le connessioni (gli archi) leggendo il tuo dizionario
    for nodo, figli in graph.items():
        for figlio in figli:
            G.add_edge(nodo, figlio)
            
    # 4. Scegliamo un "layout" (l'algoritmo che calcola le coordinate spaziali dei nodi)
    # spring_layout simula delle molle tra i nodi per distanziarli in modo leggibile
    pos = nx.spring_layout(G, seed=42)
    
    # Recuperiamo le etichette che avevamo salvato nel punto 2
    labels = nx.get_node_attributes(G, 'label')
    
    # 5. Prepariamo la "tela" di pyplot
    plt.figure(figsize=(8, 6))
    plt.title("Visualizzazione del Grafo (Nodi e Lettere)", fontsize=14, fontweight='bold')
    
    # 6. Disegniamo materialmente il grafo
    nx.draw(G, pos, 
            labels=labels, 
            with_labels=True, 
            node_size=2000,          # Grandezza dei cerchi
            node_color="#87CEFA",    # Colore azzurro chiaro
            font_size=10, 
            font_weight="bold", 
            arrowsize=20,            # Grandezza delle frecce
            edge_color="gray")       # Colore degli archi
            
    # 7. Mostriamo la finestra a schermo
    plt.show()

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
    # graph = {
    #     "1": ["2","3"],
    #     "2": ["4"],
    #     "4": ["5"],
    #     "5": ["6"],
    #     "6": ["7"],
    #     "3": ["8"],
    #     "8": ["9"],
    #     "9": ["7"]
    # }
    # etichette={
    #     "1":["A"],
    #     "2":["C"],
    #     "4":["T"],
    #     "5":["C"],
    #     "6":["T"],
    #     "7":["A"],
    #     "3":["T"],
    #     "8":["G"],
    #     "9":["A"],

    # }

    #pattern = "ACTGTA"
    plot_grafo(graph, etichette)
    fixGraph(graph, "1", etichette)
    print(graph)
    topolist = ordinaTopo(graph, "0")
    print(ordinaTopo(graph, "0"))
    m=calculateEditDistance(graph, etichette, pattern)
    print("------------------")
    printMatrix(m, topolist, pattern, etichette)
    plot_grafo(graph, etichette)
    print(backtracking(m, graph, topolist, pattern, etichette, weight=4))



main()


