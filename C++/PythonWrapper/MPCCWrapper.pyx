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

    def getInterpolatedTrack(self):
        cdef double* x_m_ptr = self._c_model.getInterpolatedTrack(0)
        cdef double[:] x_m = <double[:200]>x_m_ptr
        cdef cnp.ndarray x_m_np = np.asarray(x_m)

        cdef double* y_m_ptr = self._c_model.getInterpolatedTrack(1)
        cdef double[:] y_m = <double[:200]>y_m_ptr
        cdef cnp.ndarray y_m_np = np.asarray(y_m)

        return x_m_np, y_m_np

    def getPrediction(self):
        cdef double* x_m_ptr = self._c_model.getPrediction(0)
        cdef double[:] x_m = <double[:200]>x_m_ptr
        cdef cnp.ndarray x_m_np = np.asarray(x_m)

        cdef double* y_m_ptr = self._c_model.getPrediction(1)
        cdef double[:] y_m = <double[:200]>y_m_ptr
        cdef cnp.ndarray y_m_np = np.asarray(y_m)

        cdef double* phi_rad_ptr = self._c_model.getPrediction(2)
        cdef double[:] phi_rad = <double[:200]>phi_rad_ptr
        cdef cnp.ndarray phi_rad_np = np.asarray(phi_rad)

        cdef double* vx_mps_ptr = self._c_model.getPrediction(3)
        cdef double[:] vx_mps = <double[:200]>vx_mps_ptr
        cdef cnp.ndarray vx_mps_np = np.asarray(vx_mps)

        cdef double* vy_mps_ptr = self._c_model.getPrediction(4)
        cdef double[:] vy_mps = <double[:200]>vy_mps_ptr
        cdef cnp.ndarray vy_mps_np = np.asarray(vy_mps)

        cdef double* r_radps_ptr = self._c_model.getPrediction(5)
        cdef double[:] r_radps = <double[:200]>r_radps_ptr
        cdef cnp.ndarray r_radps_np = np.asarray(r_radps)

        cdef double* s_m_ptr = self._c_model.getPrediction(6)
        cdef double[:] s_m = <double[:200]>s_m_ptr
        cdef cnp.ndarray s_m_np = np.asarray(s_m)

        cdef double* delta_rad_ptr = self._c_model.getPrediction(7)
        cdef double[:] delta_rad = <double[:200]>delta_rad_ptr
        cdef cnp.ndarray delta_rad_np = np.asarray(delta_rad)

        cdef double* Fx_kN_ptr = self._c_model.getPrediction(8)
        cdef double[:] Fx_kN = <double[:200]>Fx_kN_ptr
        cdef cnp.ndarray Fx_kN_np = np.asarray(Fx_kN)

        cdef double* vs_mps_ptr = self._c_model.getPrediction(9)
        cdef double[:] vs_mps = <double[:200]>vs_mps_ptr
        cdef cnp.ndarray vs_mps_np = np.asarray(vs_mps)

        return x_m_np, y_m_np, phi_rad_np, vx_mps_np, vy_mps_np, r_radps_np, s_m_np, delta_rad_np, Fx_kN_np, vs_mps_np
