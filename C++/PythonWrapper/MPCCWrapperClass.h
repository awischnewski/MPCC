//
// File: MPCCWrapper.h
// Created: 30.06.2020
//
// Author: Alexander Wischnewski
// Contact: alexander.wischnewski@tum.de
//

#include <string>

#include "../MPC/mpc.h"
#include "../Params/track.h"

#include <nlohmann/json.hpp>
using json = nlohmann::json;
using namespace mpcc;

class MPCCWrapperClass {
    private:
      MPC* mpc;
    public:
      MPCCWrapperClass(std::string paramFile);
      ~MPCCWrapperClass();

      double* calcMPC(double* state_meas);
};
