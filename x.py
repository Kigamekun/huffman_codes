f = open("data_directed_graph_ipb.txt", "r")
nV, nE = f. readline().split(" ")
nV = int(nV)
nE = int (nE)
print( "Jumlah Verteks:", nV)
print("Jumlah Edge:", nE)

G = graph(nV)
G. printVertex()