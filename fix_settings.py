#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import xml.dom.minidom

### README
### * Save this file as fix_settings.py in the same directory as your job script
### * Make it executable: chmod +x fix_settings.py

def generate_hostfile(pe_hostfile):
    '''Convert Univa Grid Engine hostfile to Open MPI hostfile'''

    ompi_hostfile = Path('./hostfile.{}'.format(os.getenv('JOB_ID'))).resolve()

    with open(pe_hostfile, 'r') as f, open(ompi_hostfile, 'w') as g:
        for l in f:
            hostname, nslots = l.strip().split()[:2]
            g.write('{} slots={} max-slots={}\n'.format(hostname, nslots, nslots))

    return ompi_hostfile


def fix_settings_xml(ompi_hostfile):
    '''Fix VOTCA CSG settings.xml file'''
    settings = xml.dom.minidom.parse('settings.xml')
    print(settings.getElementsByTagName('command')[0].childNodes[0].data)

    settings.getElementsByTagName('command')[0].childNodes[0].data = '/mnt/HA/opt/openmpi/intel/2015/1.8.1-mlnx-ofed/bin/mpirun -x LD_LIBRARY_PATH -x BASH_ENV --hostfile {} gmx_mpi mdrun'.format(ompi_hostfile)

    ### XXX caution - this overwrites the settings.xml file
    with open('settings.xml', 'w') as f:
        f.write(settings.toxml())


if __name__ == '__main__':
    pe_hostfile = Path(os.getenv('PE_HOSTFILE'))
    ompi_hostfile = generate_hostfile(pe_hostfile)
    fix_settings_xml(ompi_hostfile)
