import numpy as np
import matplotlib.pyplot as plt
import os

def length(Z): return np.sqrt((Z*Z).sum())
def normalize(Z): return Z / length(Z)


# Parameters
rseed = 2
n_iter = 1000
speed_norm  = 1.00
accel_norm  = 0.1
p0 = -50 * np.ones(2)                                           # Initial position
target = np.zeros(2)                                            # Target position
v0 = -speed_norm * normalize(np.ones(2))                        # Initial velocity



plt.figure(figsize=(12,3))

## Simulation for each value of initial delay (delay corresponds to velocity application)
for i,delay in enumerate([0,20,40,60]):

    # Initialisations
    np.random.seed(rseed)
    p, v = p0, v0
    P = [p]
   
    for j in range(n_iter):
        a = accel_norm * normalize(np.random.normal(0,1,2))
        v_ = speed_norm * normalize(v + a)
        
        # Velocity is updated if new velocity leads to a more favourable result
        if length(p + v_ - target) < length( p + v - target):
            v = v_
            
        # Position is displaced w.r.t. velocity only after the period of initial delay
        if j >= delay:
            p = p + v
        P.append(p)
        
        # Simulation is stopped when position is close to the target (closeness is arbitrarily fixed) 
        if length(p - target) < 1:
            break;
        
    # Plotting
    P = np.array(P)
    ax = plt.subplot(1, 4, 1+i, aspect=1)
    ax.set_xlim(-105,25)
    ax.set_xticks([])
    ax.set_ylim(-85,45)
    ax.set_yticks([])
    
    plt.plot(P[::,0,], P[::,1], "-", color="black", linewidth=1)
    plt.plot(P[::5,0,], P[::5,1], "o", markersize=5,
             linewidth=.5, markerfacecolor="white", markeredgecolor="black")


    plt.plot( [p0[0], p0[0] + 10*v0[0]],
              [p0[1], p0[1] + 10*v0[1]], color="black", linewidth=2)

    plt.scatter([p0[0]], [p0[1]], s=25,
                edgecolor="black", facecolor="black", zorder=10)
    
    plt.scatter([target[0]], [target[1]], s=50,
                edgecolor="black", facecolor="yellow", zorder=10)

    plt.text(p0[0]+5, p0[1], "Initial\nposition",
             va = "center", ha = "left")

    plt.text(target[0], target[1]+5, "Target",
             va = "bottom", ha = "center")

    plt.text(0.01, .99, "Delay %d" % delay, weight="bold",
             va = "top", ha = "left", transform=ax.transAxes)

    # Reward contour
    X, Y = np.meshgrid(np.linspace(-150,50,100),
                       np.linspace(-150,50,100))
    Z = np.sqrt(X**2 + Y**2)
    plt.contourf(X, Y, Z, 10, cmap='gray', alpha=0.25)

    
plt.tight_layout()
plt.savefig("illustration_inertia.pdf")
plt.show()

