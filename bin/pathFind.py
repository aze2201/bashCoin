# Python program to print all paths from a source to destination.
# First networkx library is imported
# along with matplotlib
import networkx as nx
import matplotlib.pyplot as plt
import sys

#python2 Documents/qaralama/findPath.py '{"peers": [["161.97.69.136", "194.135.154.14"],["161.97.69.136", "194.135.154.12"],["194.135.154.12", "194.135.154.13"], ["194.135.154.13", "161.97.69.136"]]}'  '161.97.69.136' '161.97.69.136'


from collections import defaultdict

# This class represents a directed graph
# using adjacency list representation
class Graph:
	def __init__(self, vertices):
		# No. of vertices
		self.V = vertices
		# default dictionary to store graph
		self.graph = defaultdict(list)
	# function to add an edge to graph
	
	def addEdge(self, u, v):
		self.graph[u].append(v)
	'''A recursive function to print all paths from 'u' to 'd'.
	visited[] keeps track of vertices in current path.
	path[] stores actual vertices and path_index is current
	index in path[]'''

	def printAllPathsUtil(self, u, d, visited, path):
		# Mark the current node as visited and store in path
		visited[u]= True
		path.append(u)
		# If current vertex is same as destination, then print
		# current path[]
		if u == d:
			print (path)
		else:
			# If current vertex is not destination
			# Recur for all the vertices adjacent to this vertex
			for i in self.graph[u]:
				if visited[i]== False:
					self.printAllPathsUtil(i, d, visited, path)	
		# Remove current vertex from path[] and mark it as unvisited
		path.pop()
		visited[u]= False
	# Prints all paths from 's' to 'd'
	def printAllPaths(self, s, d):
		if d < s:
			# 2(d) < 7(s)
			# tmp=2
			# s=2
			# d=
			tmp=s
			s=d
			d=tmp 
		# Mark all the vertices as not visited
		visited =[False]*(self.V)
		# Create an array to store paths
		path = []
		# Call the recursive helper function to print all paths
		self.printAllPathsUtil(s, d, visited, path)


# Defining a Class (No use. Just in case)
class GraphVisualization:

	def __init__(self):
		
		# visual is a list which stores all
		# the set of edges that constitutes a
		# graph
		self.visual = []
		
	# addEdge function inputs the vertices of an
	# edge and appends it to the visual list
	def addEdge(self, a, b):
		temp = [a, b]
		self.visual.append(temp)
		
	# In visualize function G is an object of
	# class Graph given by networkx G.add_edges_from(visual)
	# creates a graph with a given list
	# nx.draw_networkx(G) - plots the graph
	# plt.show() - displays the graph
	def visualize(self):
		G = nx.Graph()
		G.add_edges_from(self.visual)
		nx.draw_networkx(G)
		plt.show()

# Driver code
#G = GraphVisualization()
#G.addEdge(1, 2)
#G.addEdge(2, 3)
#G.addEdge(3, 4)
#G.addEdge(2, 4)
#G.addEdge(4, 5)
#G.addEdge(5, 6)
#G.addEdge(5, 7)


# Create a graph given in the above diagram
g = Graph(8)
g.addEdge(1, 2)
g.addEdge(2, 3)
g.addEdge(3, 4)
g.addEdge(2, 4)
g.addEdge(4, 5)
g.addEdge(5, 6)
g.addEdge(5, 7)


s = 7 ; d = 1
print ("Following are all different paths from % d to % d :" %(s, d))
g.printAllPaths(s, d)
#G.visualize()
