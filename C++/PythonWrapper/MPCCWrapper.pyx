from MPCCWrapperClass cimport *
import numpy as np
cimport numpy as cnp

cdef class MPCCWrapper:
    cdef MPCCWrapperClass *_c_model

    def __cinit__(self, paramFile):
        self._c_model = new MPCCWrapperClass(paramFile.encode('UTF-8'))

    def __dealloc__(self):
        if self._c_model != NULL:
            del self._c_model

    def calcMPC(self, cnp.ndarray[double, ndim=1, mode='c'] state):
        cdef double* input_ptr = self._c_model.calcMPC(&state[0])
        cdef double[:] input = <double[:3]>input_ptr
        cdef cnp.ndarray input_np = np.asarray(input)
        return input_np
