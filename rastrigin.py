import numpy as np
from plotting.plots import make_animation_frames,plot_dead
from pypolychord import priors,run_polychord
import pypolychord.settings as settings
import os
import anesthetic

def rastrigin(x,scale):
    #vectorized 2d rastrigin function
    x1=x[...,0]
    x2=x[...,1]
    return (20*scale - np.sum(x**2- scale * np.cos(2*np.pi*x),axis=-1))
    # return -((x1**2+x2-11)**2 + (x1+x2**2-7)**2)/(2*scale**2)

#make a grid in mpl
grid = np.mgrid[-5:5:.1, -5:5:.1]
gridstack= np.dstack(grid)

#scale adjusts depth of "eggbox"
scale=5
#rastrigin ~cosine, so we don't want the rastrigin as the logl, rather as the target
z=rastrigin(gridstack,scale)
target_directory="rastrigin"

#wrap up likelihood and prior, plys set polychord settings
prior = priors.UniformPrior(-5,5)
def loglike(theta):
    return float(np.log(rastrigin(theta,scale))), []

settings=settings.PolyChordSettings(nDims=2,nDerived=0)
#rastrigin needs a lot of live points
settings.nlive=1000
settings.read_resume=False
settings.write_resume=False
settings.base_dir=os.path.join(target_directory,"chains")
run_polychord(loglike,prior=prior,nDims=2,nDerived=0,settings=settings)

#read in nested samples
ns=anesthetic.NestedSamples(root=os.path.join(target_directory,"chains/test"))

#make the live points animation
make_animation_frames(grid,z,ns,target_directory)
#plot the dead points 
plot_dead(grid,z,ns,target_directory)