# votca_helper
Helper scripts for VOTCA CSG

VOTCA runs GROMACS, but VOTCA's utilities themselves are only multithreaded.

Since VOTCA hard codes the GROMACS invocation into an XML settings file, 
and does not give a way of reading the environment variables and passing
it onto GROMACS, the settings file needs to be modified on a per-job
basis.

This script should do it. It's kludgy.