from libcpp.string cimport string

cdef extern from "MPCCWrapperClass.h":
    cdef cppclass MPCCWrapperClass:
        MPCCWrapperClass(string paramFile) except +
        double* calcMPC(double* state_meas)
        double* getPrediction(int idx)
        double* getInterpolatedTrack(int idx)
