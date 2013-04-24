PartModellingSystem
===================

Simulation for making the best shape for robot parts.

It reguires OpenDynamicsEngine. To install it and python bindings:

1. tar xf ode-0.12.tar.gz
2. cd ode-0.12
3. ./configure --enable-double-precision --with-trimesh=opcode --enable-new-trimesh --enable-shared
4. make
5. sudo make install
6. cd bindings/python/
7. python setup.py build_ext
8. python setup.py install

ode-0.12.tar.gz can be downloaded from http://sourceforge.net/projects/opende/files/
