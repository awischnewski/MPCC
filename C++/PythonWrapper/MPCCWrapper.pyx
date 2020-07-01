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

    def getPrediction(self):
        cdef double* x_m_ptr = self._c_model.getPrediction(0)
        cdef double[:] x_m = <double[:60]>x_m_ptr
        cdef cnp.ndarray x_m_np = np.asarray(x_m)

        cdef double* y_m_ptr = self._c_model.getPrediction(1)
        cdef double[:] y_m = <double[:60]>y_m_ptr
        cdef cnp.ndarray y_m_np = np.asarray(y_m)

        cdef double* v_mps_ptr = self._c_model.getPrediction(3)
        cdef double[:] v_mps = <double[:60]>v_mps_ptr
        cdef cnp.ndarray v_mps_np = np.asarray(v_mps)

        cdef double* delta_rad_ptr = self._c_model.getPrediction(7)
        cdef double[:] delta_rad = <double[:60]>delta_rad_ptr
        cdef cnp.ndarray delta_rad_np = np.asarray(delta_rad)

        cdef double* Fx_kN_ptr = self._c_model.getPrediction(8)
        cdef double[:] Fx_kN = <double[:60]>Fx_kN_ptr
        cdef cnp.ndarray Fx_kN_np = np.asarray(Fx_kN)

        return x_m_np, y_m_np, v_mps_np, delta_rad_np, Fx_kN_np
