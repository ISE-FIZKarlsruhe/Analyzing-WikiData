
# coding: utf-8

# In[1]:


import igraph as ig
import csv
from collections import defaultdict
from collections import namedtuple
import community
import networkx as nx
import numpy as np
import operator
import pydot
import plotly.plotly as py
import plotly.graph_objs as go
from networkx.drawing.nx_pydot import write_dot
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.drawing.nx_pydot import pydot_layout
import matplotlib.pyplot as plt
import matplotlib
import plotly
import plotly.offline as pyo
import math
import random
import re
plotly.tools.set_credentials_file(username='pcsplotly', api_key='ofJJAPLfVgSYzk4mmyzi')
import argparse

### INFO ###
#running on python 3.5
#inputfile is .csv

####File parameter
#----------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('project_path', type=str, nargs='?', help="specifies the path in which all three imput files are located. Needs trailing slash", default="../project_japanese/", action="store")
parser.add_argument('topic', type=str, nargs='?', help="specifies the topic name.", default="Japanese", action="store")
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
args = parser.parse_args()

#-----------------------------------
filepath = args.project_path
topic = args.topic
#-----------------------------------

louvainoutput = "louvain_clean_names.csv"
overlapgraph = "overlapgraph_clean"
finished = "finished"


# In[2]:


##Building the main dictionary from the louvainoutput file
threshold = 501


# In[3]:


ig.__version__  #requires version 0.7.1


# In[4]:


nx.__version__ #requires version 1.11


# In[5]:


plotly.__version__ #requires 2.7.0


# # Loading the Louvain Output 
# ## and convert it into a dictionary of node:partition

# In[6]:


belowthreshold = []
sizes = defaultdict()
partitioning = defaultdict()
print(filepath+louvainoutput)
with open(filepath+louvainoutput, "rt", encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        partition=row.pop(0)
        size=int(row.pop(0))
        if size < threshold:
                belowthreshold.append(partition)
        else:
            sizes[partition] = size
        for node in row:
            partitioning[node] = partition
           


# In[7]:


total_incluster = 0
for _,x in sizes.items():
    total_incluster += x
clustercount = len(sizes.items())


# In[8]:


# Parsing the 'finished' file
clustering_meta_tex = ["Total count in knowledgebase: ","Entities in overlapgraph: ","Entities in large clusters: ","<br>Clusters: ","Avg cluster size: ","Threshold: "]
clustering_meta_num = []
clusterinformation = defaultdict()
Cluster = namedtuple('info', ['size', 'score', 'example_members', 'top_attributes'], verbose=False)
with open(filepath+finished, encoding="utf8") as f:
    i = 0
    for line in f:
        i += 1
        if i>4 and i<10:
            clustering_meta_num.append("<b>"+str(int(float(re.findall(r'\d+\.?\d*', line)[0])))+"</b>")
        else:
            if line.startswith("Cluster No."):
                j = 0 # counter for how many attributes will be viewed/added
                u = 0 # counter for how many unique attributes will be viewed/added
                info = re.findall(r'\d+\.?\d*', line)
                #print(info)
                name = int(info[0])
                size = int(info[1])
                nonpart = int(info[2])
                avg_cov = float(info[3])
                max_cov = int(info[4])
                #summing the inverse of non
                score = ((1-(nonpart/size))*100)+(avg_cov*10)+(max_cov*10)
                clusterinformation[name] = Cluster(size=size, score=score, example_members=[],top_attributes=[])
            
            #get the to ranked attributes
            if line.startswith("("):
                j += 1
                s_line = line[1:].split(',')
                if j <= 3:
                    clusterinformation[name].top_attributes.append(str("Q"+s_line[0]+s_line[1]))
            
            #get the max coverage members
            if line.startswith("Max Coverage Members:"):
                # add the first 3 max coverage members
                for n in re.findall(r'\d+', line)[:3]:
                    clusterinformation[name].example_members.append(str("Q"+n))
    
    #overwrite the meta information drawn from the 'finished' file with the corret ones remaining in the final clusters
    clustering_meta_num[2] = "<b>"+str(total_incluster)+"</b>"
    clustering_meta_num[3] = "<b>"+str(clustercount)+"</b>"
    clustering_meta_num[4] = "<b>"+str(int(total_incluster/clustercount))+"</b>"
    clustering_meta_num.append("<i>"+str(threshold)+"</i>")
    
    clustering_meta = "<br>".join([tex+num for tex,num in zip(clustering_meta_tex,clustering_meta_num)])


# ## Loading the overlapgraph as a proper nx graph

# In[9]:


def buildWeightedGraph():
    print("Building weighted graph from %s..." % (filepath+overlapgraph))
    fh = open(filepath+overlapgraph, 'rb')
    G = nx.read_weighted_edgelist(fh, delimiter=";")
    print("Done.")
    return G

if True:
    original = buildWeightedGraph()


# ### check if overlapgraph and partitioning are consitent

# In[10]:


#membersinoverlap = list(map(int, original.nodes()))
#uniqueinoverlap = list(set(membersinoverlap) - set(map(int,partitioning.keys())))
#uniqueinclustrering = list(set(map(int,partitioning.keys())) - set(membersinoverlap))
#bool(uniqueinclustrering) == bool(uniqueinoverlap) == False


# ## Build the induced graph based on the partitioning and the original graph

# In[11]:

print("Building the induced graph based on the partitioning and the original graph...")
## get induced graph for all clusters
if True:
    induced = community.induced_graph(partitioning, original)
    # Save induced graph
    nx.write_gpickle(induced, filepath+"clustering_induced_graph.pkl")	
else:
    induced = nx.read_gpickle(filepath+"clustering_induced_graph.pkl")	


# In[12]:


# removing too small clusters
induced.remove_nodes_from(belowthreshold)


sorted_sizes=[x for _,x in sorted(sizes.items(), key=lambda kv: kv[1], reverse=True)]
max_size = max(sorted_sizes)
min_size = min(sorted_sizes)

def normalize(value, max_size=max_size, min_size=min_size):
    return (value - min_size) / (max_size-min_size)

normalized_sizes = defaultdict()
for key,value in sizes.items():
    normalized_sizes[key]=normalize(value)


# In[14]:


# adding the size attribute
nx.set_node_attributes(induced, "size", sizes)

# adding the normalized size attribute
nx.set_node_attributes(induced, "normalized_size", normalized_sizes)

# adding current (louvain) name as attribute
nx.set_node_attributes(induced, 'louvain_name', dict(zip( induced.nodes(),  induced.nodes())))


# In[15]:


# size mapping <oldname><sizerank>  /ranking by size and relabelling
mapping = dict(zip([x for x,_ in sorted(sizes.items(), key=lambda kv: kv[1], reverse=True)], range(0, induced.number_of_nodes())))
induced_relabeled = nx.relabel_nodes(induced, mapping)


# In[16]:


# export to .dot
nx.write_graphml(induced_relabeled,filepath+'induced.graphml') # Export NX graph to file
induced_ig = ig.read(filepath+'induced.graphml',format="graphml") # Create new IG graph from file


# # Plotting Nx Graph in 2D

# In[17]:


# generate positions for the nodes (standard layout)
pos=pydot_layout(induced_relabeled,prog='dot')

# generate positions for the nodes (spring/force layout)
force_pos = {key:(value[0],value[1]) for key,value in nx.spring_layout(induced_relabeled,scale=10000).items()}

# generate positions for the nodes (spectral layout)
circular_pos = {key:(value[0],value[1]) for key,value in nx.circular_layout(induced_relabeled,scale=10000).items()}

# add these positions as node features
nx.set_node_attributes(induced_relabeled, "pos", pos)


# In[18]:


# calculate general position infos on the whole graph
dmin=1
ncenter=0
for n in pos:
    x,y=pos[n]
    d=(x-0.5)**2+(y-0.5)**2
    if d<dmin:
        ncenter=n
        dmin=d
        
p=nx.single_source_shortest_path_length(induced_relabeled,ncenter)


# In[19]:


edge_weights = []

for u,v in induced_relabeled.edges():
    if u != v:
        edge_weights.append(math.log(induced_relabeled.get_edge_data(u,v)["weight"]+1))
    else:
        edge_weights.append(0)
        
max_log_edgeweight=max(edge_weights)


# In[20]:


edge_weights = norm = [float(i)/max(edge_weights)*5 for i in edge_weights]


# ## Create Edges

# In[21]:


#edge_trace = go.Scatter(
#    x=[],
#    y=[],
#    line=dict(width=0.5,color='#888'),
#    text=dumm_edge_weights,
#    hoverinfo="text",
#    mode='lines')
#
#for edge in induced_relabeled.edges():
#    x0, y0 = induced_relabeled.node[edge[0]]['pos']
#    x1, y1 = induced_relabeled.node[edge[1]]['pos']
#    edge_trace['x'] += [x0, x1, None]
#    edge_trace['y'] += [y0, y1, None]

edge_traces = []

for edge,weight in zip(induced_relabeled.edges(),edge_weights):
    x0, y0 = induced_relabeled.node[edge[0]]['pos']
    x1, y1 = induced_relabeled.node[edge[1]]['pos']
    edge_traces.append(go.Scatter(
    x=[x0, x1, None],
    y=[y0, y1, None],
    line=dict(width=weight,color='#888'),
    text = str(weight),
    hoverinfo ='text',
    mode='lines'))


node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for node in induced_relabeled.nodes():
    x, y = induced_relabeled.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)


# ## Manipulate Edge Appearance

# ## Create Node Appearance and Info

# In[22]:


#individual node setting
colors = []
descriptions = []
node_sizes = []
sizefactor = 50
for node, adjacencies in enumerate(induced_relabeled.adjacency_list()):
    colors.append(len(adjacencies))
    
    #add the nodes hover info
    node_info = 'Node no: '+str(node)+'<br>Size: '+str(induced_relabeled.node[node]['size'])+'<br># of connections: '+str(len(adjacencies))+'<br>Louvain id: '+str(induced_relabeled.node[node]['louvain_name'])
    
    descriptions.append(node_info)
    #node_sizes = list(map(lambda v : (v+1)*sizefactor,normalized_sizes))
    node_sizes.append((induced_relabeled.node[node]['normalized_size']+1)*sizefactor)
    
node_trace['marker']['color'] = colors
node_trace['text'] = descriptions
node_trace['marker']['size'] = node_sizes
    


# ## Create/Draw Network Graph
# 

# In[23]:


#fig = go.Figure(data=[*edge_traces, node_trace],
#             layout=go.Layout(
#                title='<br>Network graph',
#                titlefont=dict(size=16),
#                showlegend=False,
#                hovermode='closest',
#                margin=dict(b=20,l=5,r=5,t=40),
#                annotations=[ dict(
#                    text="...",
#                    showarrow=False,
#                    xref="paper", yref="paper",
#                    x=0.005, y=-0.002 ) ],
#                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
#
#py.iplot(fig, filename='networkx')
#pyo.plot(fig, filename='networkx')


# <br><br><br><br>
# # igraph

# In[24]:


#[n for n in induced_relabeled.node.values()]


# In[25]:


N = len(induced_relabeled.nodes())
#layt=induced_ig.layout('circular_3d')
layt=induced_ig.layout('kk',dim=3)


# In[26]:


scale=1

Xn=[layt[k][0]*scale for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1]*scale  for k in range(N)]# y-coordinates
Zn=[layt[k][2]*scale  for k in range(N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]


#for e in induced_ig.get_edgelist():
#    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
#    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
#    Ze+=[layt[e[0]][2],layt[e[1]][2], None]


# In[27]:


#new single edge traces with weights and annotations
edge_traces_3d = []
    
for edge in induced_ig.es:
    source_vertex_id = edge.source
    target_vertex_id = edge.target
    Xe=[layt[source_vertex_id][0],layt[target_vertex_id][0], None]# x-coordinates of edge ends
    Ye=[layt[source_vertex_id][1],layt[target_vertex_id][1], None]
    Ze=[layt[source_vertex_id][2],layt[target_vertex_id][2], None]
    if source_vertex_id == target_vertex_id:
        weight = 0
    else:
        weight = (math.log(edge['weight'])/max_log_edgeweight)*10
        #weight = ((edge['weight'])/math.exp(max_log_edgeweight))*10
        #weight = random.random()*50
        
    edge_traces_3d.append(go.Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=dict(color='rgb(125,125,125)', 
               width=weight/2),
               text=str(round(edge['weight'])),
               hoverinfo='none'
               ))


# ## Nodes

# In[28]:


#clusterinformation.keys()


# In[29]:


##Original edge trace
#trace1=go.Scatter3d(x=Xe,
#               y=Ye,
#               z=Ze,
#               mode='lines',
#               line=dict(color='rgb(125,125,125)', width=1),
#               hoverinfo='none'
#               )

##Node descriptions
descriptions = []
for k in range(N):
    ln = int(induced_relabeled.node[k]['louvain_name'])
    description = "<b>Size:</b> "+str(clusterinformation[ln].size)+    "<br><b>Top Attributes:</b><br>"+"".join([a+"<br>" for a in clusterinformation[ln].top_attributes])+    "<br><b>Examples:</b><br>"+str(clusterinformation[ln].example_members) 
    descriptions.append(description)

#node trace
node_trace_3d =go.Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='clusters',
               marker=dict(symbol='dot',
                             size=[x/2 for x in node_sizes],
                             color=colors,
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=descriptions,
               hoverinfo='text'
               )

#heading trace
label_trace_3d =go.Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='text',
               text=[n['louvain_name'] for n in induced_relabeled.node.values()],
               #text= [clusterinformation[int(n['louvain_name'])] for n in induced_relabeled.node.values()], 
               hoverinfo='none'
               )


# In[30]:


axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title='')


# In[31]:


layout = go.Layout(
         title=topic+" - Clustering (3D visualization)",
         width=1600,
         height=900,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ),
     margin=dict(
        t=100
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text=clustering_meta,
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ],    )


# In[32]:


data=[*edge_traces_3d, node_trace_3d,label_trace_3d]
fig=go.Figure(data=data, layout=layout)


#py.iplot(fig, filename='3D')
pyo.plot(fig, filename=filepath+str(topic.lower()+'_3D.html'))
print("3D-plot created.")
