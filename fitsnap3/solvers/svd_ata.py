from .solver import Solver
from ..parallel_tools import pt
from ..io.input import config
from scipy.linalg import lstsq
import numpy as np


class SVD_ATA(Solver):

    def __init__(self, name):
        super().__init__(name)

    def perform_fit(self):
        if pt.shared_arrays['configs_per_group'].testing_elements != 0:
            testing = -1*pt.shared_arrays['configs_per_group'].testing_elements
        else:
            testing = len(pt.shared_arrays['w'].array)
        w = pt.shared_arrays['w'].array[:testing]
        aw, bw = w[:, np.newaxis] * pt.shared_arrays['a'].array[:testing], w * pt.shared_arrays['b'].array[:testing]        
        if config.sections['EXTRAS'].apply_transpose:
            bw = aw.T@bw
            aw = aw.T@aw
        self.fit, residues, rank, s = lstsq(aw, bw, 1.0e-13)
        
    def perform_atafit(self):
        #awidth = pt.Ae.shape[0]
        #nfiles = pt.Ae.shape[2]
        #A = np.zeros((awidth, awidth))
        #for i in range(nfiles):
        #    A = A + pt.Ae[:,:,i] + pt.Af[:,:,i] + pt.Av[:,:,i]        
        #print(A-pt.shared_arrays['ata'].array)

        fileAe = open('Ae.bin', 'wb');
        pt.Ae = pt.Ae.flatten(order = 'F');
        pt.Ae.astype('float64').tofile(fileAe);
        fileAe.close();
        fileAf = open('Af.bin', 'wb');
        pt.Af = pt.Af.flatten(order = 'F');
        pt.Af.astype('float64').tofile(fileAf);
        fileAf.close();
        fileAv = open('Av.bin', 'wb');
        pt.Av = pt.Av.flatten(order = 'F');
        pt.Av.astype('float64').tofile(fileAv);
        fileAv.close();
        filebe = open('be.bin', 'wb');
        pt.be = pt.be.flatten(order = 'F');
        pt.be.astype('float64').tofile(filebe);
        filebe.close();
        filebf = open('bf.bin', 'wb');
        pt.bf = pt.bf.flatten(order = 'F');
        pt.bf.astype('float64').tofile(filebf);
        filebf.close();
        filebv = open('bv.bin', 'wb');
        pt.bv = pt.bv.flatten(order = 'F');
        pt.bv.astype('float64').tofile(filebv);
        filebv.close();

        ata = 0.5*(pt.shared_arrays['ata'].array + pt.shared_arrays['ata'].array.T)
        atb = pt.shared_arrays['atb'].array               
        self.coeff, residues, rank, s = lstsq(ata, atb, 1.0e-13)
        #print(atb)
        #print(self.coeff)

        filea = open('ata.bin', 'wb');
        ata = ata.flatten(order = 'F');
        ata.astype('float64').tofile(filea);
        filea.close();
        fileb = open('atb.bin', 'wb');
        atb = atb.flatten(order = 'F');
        atb.astype('float64').tofile(fileb);
        fileb.close();
        filec = open('coeff.bin', 'wb');
        c = self.coeff.flatten(order = 'F');
        c.astype('float64').tofile(filec);
        filec.close();

    def _dump_a(self):
        np.savez_compressed('a.npz', a=pt.shared_arrays['a'].array)

    def _dump_x(self):
        np.savez_compressed('x.npz', x=self.fit)

    def _dump_b(self):
        b = pt.shared_arrays['a'].array @ self.fit
        np.savez_compressed('b.npz', b=b)
