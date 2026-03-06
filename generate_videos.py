# ==========================================================
# SUZUKI COSMIC VIDEO GENERATOR
# Generates scientific videos:
# 1. 11D → 3D projection
# 2. Cosmic web evolution
# 3. Black hole merger
# 4. CMB fluctuation
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.fft import fft2, ifft2, fftfreq
import os

# ----------------------------------------------------------
# setup
# ----------------------------------------------------------

os.makedirs("videos", exist_ok=True)

PHI = (1 + np.sqrt(5)) / 2

# ----------------------------------------------------------
# 11D → 3D projection video
# ----------------------------------------------------------

def projection_matrix():

    return np.array([
        [1,PHI,1/PHI,PHI**2,1,PHI,1/PHI,PHI**2,1,PHI,1/PHI],
        [PHI,1/PHI,PHI**2,1,PHI,1/PHI,PHI**2,1,PHI,1/PHI,PHI**2],
        [1/PHI,PHI**2,1,PHI,1/PHI,PHI**2,1,PHI,1/PHI,PHI**2,1]
    ])

def generate_projection_video():

    N=1000

    points11 = np.random.normal(0,1,(N,11))

    P = projection_matrix()

    fig = plt.figure()

    ax = fig.add_subplot(111,projection="3d")

    scat = ax.scatter([],[],[],s=2)

    def update(frame):

        noise = np.sin(frame*0.05)

        proj = (points11 + noise) @ P.T

        proj = proj / (np.linalg.norm(proj,axis=1)[:,None]+1e-9)

        scat._offsets3d = (proj[:,0],proj[:,1],proj[:,2])

        ax.set_xlim(-1,1)
        ax.set_ylim(-1,1)
        ax.set_zlim(-1,1)

        return scat,

    ani = FuncAnimation(fig,update,frames=200)

    ani.save("videos/11D_projection.mp4",fps=30)

# ----------------------------------------------------------
# cosmic web simulation video
# ----------------------------------------------------------

def generate_cosmic_web_video():

    N=2000

    points = np.random.normal(0,1,(N,3))

    velocity = np.zeros_like(points)

    fig = plt.figure()

    ax = fig.add_subplot(111,projection="3d")

    scat = ax.scatter([],[],[],s=2)

    def gravity(p):

        diff = p[:,None,:] - p[None,:,:]

        r = np.linalg.norm(diff,axis=2)+0.1

        force = np.sum(diff/(r[:,:,None]**3),axis=1)

        return force

    def update(frame):

        nonlocal points,velocity

        force = gravity(points)

        velocity += 0.001*force

        points += velocity

        scat._offsets3d=(points[:,0],points[:,1],points[:,2])

        ax.set_xlim(-5,5)
        ax.set_ylim(-5,5)
        ax.set_zlim(-5,5)

        return scat,

    ani = FuncAnimation(fig,update,frames=200)

    ani.save("videos/cosmic_web.mp4",fps=30)

# ----------------------------------------------------------
# black hole merger video
# ----------------------------------------------------------

def generate_blackhole_video():

    fig,ax = plt.subplots()

    t = np.linspace(0,10,400)

    x1 = -1 + 0.1*t
    x2 = 1 - 0.1*t

    y1 = np.sin(t)
    y2 = -np.sin(t)

    wave = np.sin(10*t)*np.exp(0.2*t)

    scat = ax.scatter([],[],s=200)

    line, = ax.plot([],[])

    def update(frame):

        bx=[x1[frame],x2[frame]]
        by=[y1[frame],y2[frame]]

        scat.set_offsets(np.c_[bx,by])

        line.set_data(t[:frame],wave[:frame])

        ax.set_xlim(-2,10)
        ax.set_ylim(-5,5)

        return scat,line

    ani=FuncAnimation(fig,update,frames=300)

    ani.save("videos/blackhole_merger.mp4",fps=30)

# ----------------------------------------------------------
# CMB evolution video
# ----------------------------------------------------------

def generate_cmb_video():

    size=256

    fig,ax=plt.subplots()

    img=ax.imshow(np.zeros((size,size)))

    def cmb():

        noise=np.random.normal(0,1,(size,size))

        kx=fftfreq(size)
        ky=fftfreq(size)

        KX,KY=np.meshgrid(kx,ky)

        spec=1/(KX**2+KY**2+0.01)

        return np.real(ifft2(fft2(noise)*spec))

    def update(frame):

        img.set_data(cmb())

        return img,

    ani=FuncAnimation(fig,update,frames=200)

    ani.save("videos/cmb_evolution.mp4",fps=30)

# ----------------------------------------------------------
# run all
# ----------------------------------------------------------

if __name__ == "__main__":

    print("Generating projection video")
    generate_projection_video()

    print("Generating cosmic web video")
    generate_cosmic_web_video()

    print("Generating black hole merger video")
    generate_blackhole_video()

    print("Generating CMB video")
    generate_cmb_video()

    print("All videos generated in /videos")
