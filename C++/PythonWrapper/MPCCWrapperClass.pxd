from libcpp.string cimport string

cdef extern from "MPCCWrapperClass.h":
    cdef cppclass MPCCWrapperClass:
        MPCCWrapperClass(string paramFile) except +
        void calcMPC(double* state_meas, double* input_calc)
