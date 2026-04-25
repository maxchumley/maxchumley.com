#%%

from curses import window
import numpy as np
from teaspoon.MakeData.DynSysLib.autonomous_dissipative_flows import lorenz
from teaspoon.DAF.data_assimilation import TADA
from teaspoon.DAF.forecasting import forecast_time
from teaspoon.DAF.forecasting import random_feature_map_model
from teaspoon.DAF.forecasting import get_forecast
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import rc

from IPython.display import clear_output


# Set font
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
rc('text', usetex=True)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rcParams.update({'font.size': 16})

# Set random seed
r_seed = 48824
np.random.seed(r_seed)

# Set TADA parameters
snr = 50.0
lr = 1e-7
train_len = 4000
forecast_len = 2000
window_size = 50
max_window_number = 300

# Get training and validation data at random initial condition
ICs = list(np.random.normal(size=(3,1)).reshape(-1,))
t, ts = lorenz(L=500, fs=50, SampleSize=6001, parameters=[28,10.0,8.0/3.0],InitialConditions=ICs)
ts = np.array(ts) 

# Get signal and noise amplitudes using signal-to-noise ratio
a_sig = np.sqrt(np.mean(np.square(ts),axis=1))
a_noise = a_sig * 10**(-snr/20)

# Add noise to the signal
Gamma = np.diag(a_noise)
noise = np.random.normal(size=np.shape(ts[:,0:train_len+forecast_len]))
u_obs = ts[:,0:train_len+forecast_len] + Gamma@noise

# Train model
W_LR, W_in, b_in = random_feature_map_model(u_obs[:,0:train_len],Dr=500, seed=r_seed)

# Set optimization parameters
d_rate = 0.996
opt_params = [lr, d_rate]
W_opt = W_LR 

# TADA optimization loop
for window_number in range(1,max_window_number):
    print(window_number)
    model_parameters = [W_opt, W_LR, W_in, b_in]  
    W_opt = TADA(u_obs, window_size, model_parameters, train_len=train_len, n_epochs=2, opt_params=opt_params, window_number=window_number)

    # Set forecast parameters
    start = train_len
    end = train_len + max_window_number + 1

    # Forecast TADA and LR models and get measurements
    X_model_tada = get_forecast(u_obs[:,train_len], W_opt, W_in, b_in,forecast_len=end-train_len)
    X_model_lr =get_forecast(u_obs[:,train_len], W_LR, W_in, b_in,forecast_len=end-train_len)
    X_meas = u_obs[:,start:end]

    # Plot measurements and forecast
    fig = plt.figure(figsize=(5, 3), dpi=200)

    plt.plot(X_model_tada[0,:],'r', label="Forecast")  
    plt.plot(X_meas[0,:], '.b', label="Measurement", markersize=3)

    if window_number< window_size:
        indices = np.linspace(0,window_number, window_number+1)
        plt.plot(indices, X_meas[0,0:window_number+1], '.-g', label="Measurement", markersize=8)
    elif window_number < max_window_number:
        indices = np.linspace(window_number-window_size,window_number-1, window_size)
        plt.plot(indices, X_meas[0,window_number-window_size:window_number], '.-g', label="Measurement", markersize=8)

    plt.plot([],[])
    plt.tick_params(axis='both', which='major', labelsize='x-large')
    plt.ylim((-30,30))
    plt.axis('off')

    plt.tight_layout()

    plt.savefig(f"./title_frames/{window_number}.png")
    plt.close(fig)
    # plt.show()
    # clear_output(wait=True)



#%%

# STATE SPACE ANIMATION

import numpy as np
from teaspoon.MakeData.DynSysLib.autonomous_dissipative_flows import lorenz
from teaspoon.DAF.data_assimilation import TADA
from teaspoon.DAF.forecasting import forecast_time
from teaspoon.DAF.forecasting import random_feature_map_model
from teaspoon.DAF.forecasting import get_forecast
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import rc

from IPython.display import clear_output


# Set font
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
rc('text', usetex=True)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rcParams.update({'font.size': 16})

# Set random seed
r_seed = 48824
np.random.seed(r_seed)

# Set TADA parameters
snr = 50.0
lr = 1e-7
train_len = 4000
forecast_len = 2000
window_size = 50
max_window_number = 300

# Get training and validation data at random initial condition
ICs = list(np.random.normal(size=(3,1)).reshape(-1,))
t, ts = lorenz(L=500, fs=50, SampleSize=6001, parameters=[28,10.0,8.0/3.0],InitialConditions=ICs)
ts = np.array(ts) 

# Get signal and noise amplitudes using signal-to-noise ratio
a_sig = np.sqrt(np.mean(np.square(ts),axis=1))
a_noise = a_sig * 10**(-snr/20)

# Add noise to the signal
Gamma = np.diag(a_noise)
noise = np.random.normal(size=np.shape(ts[:,0:train_len+forecast_len]))
u_obs = ts[:,0:train_len+forecast_len] + Gamma@noise

# Train model
W_LR, W_in, b_in = random_feature_map_model(u_obs[:,0:train_len],Dr=500, seed=r_seed)

# Set optimization parameters
d_rate = 0.996
opt_params = [lr, d_rate]
W_opt = W_LR 

s1 = 0
e1 = 1

# TADA optimization loop
for window_number in range(1,max_window_number):
    print(window_number)
    model_parameters = [W_opt, W_LR, W_in, b_in]  
    W_opt = TADA(u_obs, window_size, model_parameters, train_len=train_len, n_epochs=2, opt_params=opt_params, window_number=window_number)

    # Set forecast parameters
    start = train_len
    end = train_len + max_window_number + 1


    # Forecast TADA and LR models and get measurements
    X_model_tada = get_forecast(u_obs[:,train_len], W_opt, W_in, b_in,forecast_len=end-train_len)
    X_model_lr =get_forecast(u_obs[:,train_len], W_LR, W_in, b_in,forecast_len=end-train_len)
    X_meas = u_obs[:,start:end]

    # Plot measurements and forecast
    fig = plt.figure(figsize=(5, 5), dpi=200)

    a = 6e-6
    alp = -a*window_number*(window_number - max_window_number) + 0.05
    
    plt.plot(X_model_tada[0,s1:e1], X_model_tada[1,s1:e1],'r', label="Forecast", alpha=alp)  
    plt.plot(X_meas[0,s1:e1], X_meas[1,s1:e1], '.b', label="Measurement", markersize=3, alpha=alp)

    if window_number< window_size:
        indices = np.linspace(0,window_number, window_number+1)
        # plt.plot(X_meas[0,0:window_number+1], X_meas[1,0:window_number+1], '.-g', label="Measurement", markersize=8)
        s1 = 0
        e1 = window_number
    elif window_number < max_window_number:
        indices = np.linspace(window_number-window_size,window_number-1, window_size)
        # plt.plot(X_meas[0,window_number-window_size:window_number], X_meas[1,window_number-window_size:window_number], '.-g', label="Measurement", markersize=8)
        s1 = window_number-window_size
        e1 = window_number

    plt.plot([],[])
    plt.tick_params(axis='both', which='major', labelsize='x-large')
    plt.xlim(-20,20)
    plt.ylim((-30,30))
    plt.axis('off')

    plt.tight_layout()

    plt.savefig(f"./state_space_frames_transparent/{window_number}.png")
    clear_output(wait=True)

    plt.show()
    
    plt.close(fig)