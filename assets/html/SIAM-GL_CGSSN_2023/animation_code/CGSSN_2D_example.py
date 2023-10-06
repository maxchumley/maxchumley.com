# -*- coding: utf-8 -*-
#%%
"""
Created on Sun Oct 25 22:10:06 2020

@author: myersau3
"""
def get_noise_amplitude(t, x, SNR, SNR_type = 'Decibels'):
    A_signal = np.sqrt((1/(t[-1]-t[0]))*np.trapz((x-np.mean(x))**2, t))
    if SNR_type == 'Decibels': A_noise = A_signal*(10**(-(SNR/20)))
    if SNR_type == 'Normal': A_noise = A_signal/np.sqrt(SNR)
    if SNR_type != 'Decibels' and SNR_type != 'Normal':
        print('Error: SNR_type needs to be either Decibels or Normal')
        A_noise = 0
    return A_noise

def takens2(ts, n, tau):
    
    """This function generates an array of n-dimensional arrays from a time-delay state-space reconstruction.
    
    Args:
        ts (1-D array): 1-D time series signal
    
    Other Parameters:
        n (Optional[int]): embedding dimension for state space reconstruction. Default is uses FNN algorithm from parameter_selection module.
        tau (Optional[int]): embedding delay fro state space reconstruction. Default uses MI algorithm from parameter_selection module.
        
    Returns:
        [arraay of n-dimensional arrays]: array of delyed embedded vectors of dimension n for state space reconstruction.
    """
    
    import numpy as np
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'))
    
    if tau == None:
        from parameter_selection import MI_delay
        tau = MI_delay.MI_for_delay(ts, method = 'basic', h_method = 'sturge', k = 2, ranking = True)
    if n == None:
        from parameter_selection import FNN_n
        perc_FNN, n = FNN_n.FNN_n(ts, tau)
    
    
    #takens embedding method. Not the fastest algoriothm, but it works. Need to improve
    L = len(ts) #total length of time series
    SSR = []
    for i in range(L - tau * (n - 1)): 
        v_i = ts[i:i + tau * n:tau]
        SSR.append(v_i)
    return np.array(SSR)



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

t = np.linspace(0,100,2000)
# ts = np.sin(t*np.pi)
import teaspoon.MakeData.DynSysLib.DynSysLib as DSL

system = 'rossler'
dynamic_state = 'periodic'
t, ts = DSL.DynamicSystems(system, dynamic_state)
# ts = ts + np.random.normal(size=np.shape(ts),scale=0.2)
ts_0 = (np.array(ts))[2]
SNR = 30 #define signal to noise ratio (SNR) -- an SNR of 25 is considered a moderate level of noise.
sd = get_noise_amplitude(t, ts_0, SNR) #calculate the standard deviation associated to SNR
ts = ts_0 + np.random.normal(0,sd,len(t)) #add noise to signal.
tau = 6#int(0.99*MsPE_tau(ts_0))
ETS = takens(ts_0, n = 3, tau = tau)
    
x = ETS.T[0]
y = ETS.T[1]
# plt.plot(x,y,'.r')

# In[ ]:
    
#functions in development (a lot of this is copied from teaspoon and then modified).
from teaspoon.SP.network_tools import remove_zeros
from teaspoon.SP.network_tools import make_network	    
from teaspoon.SP.network_tools import make_network
from teaspoon.parameter_selection import MsPE	    
from teaspoon.parameter_selection import MsPE
import teaspoon.SP.tsa_tools as tsa_tools
from teaspoon.SP.tsa_tools import takens

SSR = takens(ts, n = 2, tau = tau)

n = 2 #dimension of SSR
B = 12 #number of states per dimension
embedding_method = 'standard' #can be standard or difference
binning_method = 'equal_size' #can be equal_size or equal_frequency

#get binnings
B_array = tsa_tools.cgss_binning(ts, n, tau, B, binning_method = binning_method)

#get adjacency matrix

#get state sequence. this step is redundant and is not necessary, but the state sequence is used for plotting purposes.
#B does not need to be provided if using OPN and only for CGSSN
SSR = tsa_tools.takens(ts, n, tau) 

S_mod = tsa_tools.cgss_sequence(SSR, B_array) #state sequence
S = np.unique(S_mod, return_inverse = True)[1] 
print(S)

N = len(np.unique(S))
A = np.zeros((N,N)) #prepares A
delay = 1
for i in range(len(S)-delay): #go through all permutation transitions (This could be faster wiuthout for loop)
    A[S[i]][S[i+delay]] += 1 #for each transition between permutations increment A_ij


min_bound = np.min(B_array)
max_bound = np.max(B_array)


# In[ ]:
    


import networkx as nx
np.random.seed(41)
X = np.copy(A)
np.fill_diagonal(X, 0)
G = nx.from_numpy_matrix(X)
c_nodes = (list(G))
G.remove_nodes_from(list(nx.isolates(G)))
edges = G.edges()
weights = [G[u][v]['weight'] for u,v in edges]
weights = np.array(weights)*2/max(weights)
its = int(300000/len(A))
print('number of graph layout iterations: ', its)
c_nodes = (list(G))
pos = nx.spring_layout(G, iterations = its, weight = 'weight')
nodes = nx.draw_networkx_nodes(G,pos, node_color = 'lightblue', node_size = 200)
                            #    with_labels = True)
nodes.set_edgecolor('k')
edges = nx.draw_networkx_edges(G,pos, width=weights)
plt.show()
G_simple = G


Nodes = list(G.nodes)
print(Nodes)
points = len(Nodes)
positions = []
for i in range(points):
    pos_i = np.array(pos[Nodes[i]])
    positions = np.append(positions,pos_i)
positions = np.reshape(positions,(int(len(positions)/2),2)).T


# In[ ]:
framecount = -1
window = 3.5
start = True
t = t-t[0]
TextSize = 25
plotting = True
if plotting == True:
    Ai = np.zeros((len(A[0]), len(A[0])))
    for i in range(199,200, 1):
        framecount = framecount+1
        wid = 15.5
        hig = 3.9
        MS = 10
        plt.figure(figsize=(wid,hig))
        Q = 150
        gs = gridspec.GridSpec(1, 11) 
        
        
        # ax = plt.subplot(gs[0, 0:4]) #plot time series
        # plt.plot(t,ts[0],'k')
        # plt.xlim(0,(t[i])+1.7*window)
        # plt.xticks(size = TextSize)
        # plt.ylabel('$x(t)$', size = TextSize)
        # plt.xlabel('$t$', size = TextSize)
        # plt.yticks(size = TextSize)
        # # plt.grid()
        
        
        ax = plt.subplot(gs[0, 5:8]) #plot time series
        c = 'black'
        for boundary in B_array:
            plt.plot([min_bound, max_bound], [boundary, boundary], 'k:')
            plt.plot([boundary, boundary], [min_bound, max_bound], 'k:')
        for i in range(2000):
            x_node_pos = S_mod[i]%B
            y_node_pos = int(S_mod[i]/B)
            node_width = 2.5
            plt.plot([B_array[x_node_pos], B_array[x_node_pos] + node_width], [B_array[y_node_pos], B_array[y_node_pos]], 'k:')
            plt.plot([B_array[x_node_pos], B_array[x_node_pos]], [B_array[y_node_pos], B_array[y_node_pos]+node_width], 'k:')
            
            ax.fill_between([B_array[x_node_pos], B_array[x_node_pos] + node_width],
                            [B_array[y_node_pos], B_array[y_node_pos]],
                            [B_array[y_node_pos] + node_width, B_array[y_node_pos] + node_width],
                            color = 'lightcoral', alpha = 0.99)
        plt.plot(x, y, color=c)
        plt.xticks([], size = TextSize)
        plt.yticks([], size = TextSize)
        
        plt.xlim(0,30)
        plt.ylim(0,30)
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.xlabel(r'$x(t_i)$', size = TextSize)
        plt.ylabel(r'$x(t_{i+\tau})$', size = TextSize)
        

        ax = plt.subplot(gs[0, 8:11]) #plot time series
        if S[i] != S[i-1]:
            Ai[S[i]-1][S[i-1]-1] += 1
        ind = np.nonzero(Ai > 0)
        MS = 70
        x_c = positions[0]
        y_c = positions[1]
        if i > 0: 
            for j in range(1,i+1):
                J0 = S[j-1]
                J1 = S[j]
                plt.plot([x_c[J0], x_c[J1]],[y_c[J0], y_c[J1]], 'k',zorder=0, alpha = 1)
                plt.scatter(x_c[J0], y_c[J0], color = 'black', s = int(MS*1.8))
                plt.scatter(x_c[J0], y_c[J0], color = '#A0CBE2', s = MS)
                plt.scatter(x_c[J1], y_c[J1], color = 'black', s = int(MS*1.8))
                plt.scatter(x_c[J1], y_c[J1], color = '#A0CBE2', s = MS)
        plt.axis('off')
        plt.xlim(-1.1,1.1)
        plt.ylim(-1.1,1.1)
        
        
        
        print('time: ', t[i], '  --    i: ', i ,'/', len(t)-1)
        plt.subplots_adjust(wspace= 0.4)
        # plt.savefig('C:\\Users\\myersau3.EGR\\Desktop\\python_png\\example_periodic_2D_CGSSN.png', 
        #     bbox_inches='tight',dpi = 300) 
        plt.show()
        
        
# In[ ]:
framecount = -1
window = 3.5
start = True
t = t-t[0]
TextSize = 22
plotting = True
if plotting == True:
    Ai = np.zeros((len(A[0]), len(A[0])))
    for i in range(0,200, 1):
        framecount = framecount+1
        wid = 18
        hig = 4.5
        MS = 10
        plt.figure(figsize=(wid,hig))
        Q = 150
        gs = gridspec.GridSpec(1, 11) 
        
        # ax = plt.subplot(gs[0, 0:4]) #plot time series
        # plt.plot(t,ts,'k')
        
        # plt.plot([-100, t[i]], [ts[i], ts[i]], 'r--')
        # plt.plot([-100, t[i+tau]], [ts[i+tau], ts[i+tau]], 'b--')
        # plt.plot([t[i]], [ts[i]], 'ro', markersize= MS-2, label = '$x(t_i)$')
        # plt.plot([t[i+tau]], [ts[i+tau]], 'bo', markersize= MS-2, label = r'$x(t_{i+\tau})$')
        # plt.xlim((t[i]-0.5*window),(t[i])+1.7*window)
        # plt.xticks([])
        # plt.ylabel('$x(t)$', size = TextSize)
        # plt.xlabel('time', size = TextSize)
        # plt.yticks(size = TextSize)
        # plt.grid()
        # for spine in plt.gca().spines.values():
        #     spine.set_visible(False)
        # plt.legend(loc= 'upper right', fontsize = TextSize)
        
        
        
        
        
        
        ax = plt.subplot(gs[0, 5:8]) #plot time series
        c = 'black'
        
        for boundary in B_array:
            plt.plot([min_bound, max_bound], [boundary, boundary], 'k:', alpha=0.5)
            plt.plot([boundary, boundary], [min_bound, max_bound], 'k:', alpha=0.5)
        #plt.xlim(min_bound, max_bound)
        #plt.ylim(min_bound, max_bound)
        x_node_pos = S_mod[i]%B
        y_node_pos = int(S_mod[i]/B)
        print(x_node_pos, y_node_pos)
        # Create a Rectangle patch
        node_width = 0.32
        ax.fill_between([B_array[x_node_pos], B_array[x_node_pos] + node_width],
                        [B_array[y_node_pos], B_array[y_node_pos]],
                        [B_array[y_node_pos] + node_width, B_array[y_node_pos] + node_width],
                        color = 'red', alpha = 0.7)

        plt.plot(x, y, color=c)
        # plt.plot([-100, x[i]], [y[i], y[i]], 'b--')
        # plt.plot([x[i], x[i]], [-100, y[i]], 'r--')
        plt.plot(x[i], y[i], 'ko', markersize= MS+5)
        plt.plot(x[i], y[i], 'wo', markersize= MS)
        plt.xticks([], size = TextSize)
        plt.yticks([], size = TextSize)
        plt.xlabel(r'$x(t_i)$', size = TextSize)
        plt.ylabel(r'$x(t_{i+\tau})$', size = TextSize)
        plt.xlim(-1.7,1.7)
        plt.ylim(-1.7,1.7)
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        
        
        
        
        ax = plt.subplot(gs[0, 8:11]) #plot time series
        
        if S[i] != S[i-1]:
            Ai[S[i]-1][S[i-1]-1] += 1
        ind = np.nonzero(Ai > 0)

        MS = 70
        x_c = positions[0]
        y_c = positions[1]
            
        
        
        plt.scatter(x_c[S[i]],y_c[S[i]], color = 'red', s = int(MS*3.5), alpha = 0.7)
        if i > 0: 
            for j in range(1,i+1):
                J0 = S[j-1]
                J1 = S[j]
                plt.plot([x_c[J0], x_c[J1]],[y_c[J0], y_c[J1]], 'k',zorder=0, alpha = 1)
                plt.scatter(x_c[J0], y_c[J0], color = 'black', s = int(MS*1.8))
                plt.scatter(x_c[J0], y_c[J0], color = '#A0CBE2', s = MS)
                plt.scatter(x_c[J1], y_c[J1], color = 'black', s = int(MS*1.8))
                plt.scatter(x_c[J1], y_c[J1], color = '#A0CBE2', s = MS)
        
    
        plt.axis('off')
        plt.xlim(-1.1,1.1)
        plt.ylim(-1.1,1.1)


        print('time: ', t[i], '  --    i: ', i ,'/', len(t)-1)
        plt.subplots_adjust(wspace= 0.4)
        plt.savefig('./frames/frame'+str(framecount)+'.png', bbox_inches='tight',dpi = 200)
        plt.show()

# In[ ]:    

make_gif = True
if make_gif == True:
    
    import imageio
    images = []
    for i in range(113):
        images.append(imageio.imread('./frames/frame'+str(i)+'.png'))
    imageio.mimsave('CGSSN_2d_example_cycle.gif', images, fps = 6)

    import moviepy.editor as mp
    #clip = mp.VideoFileClip('CGSSN_2d_example_cycle.gif')
    #clip.write_videofile("CGSSN_2d_example_cycle.mp4")
