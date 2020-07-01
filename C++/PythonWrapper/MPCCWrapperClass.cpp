#include "MPCCWrapperClass.h"

MPCCWrapperClass::MPCCWrapperClass(std::string paramFile)
{
    // load parameter files from json
    std::ifstream iConfig(paramFile);

    json jsonConfig;
    iConfig >> jsonConfig;

    PathToJson json_paths {jsonConfig["model_path"],
                               jsonConfig["cost_path"],
                               jsonConfig["bounds_path"],
                               jsonConfig["track_path"],
                               jsonConfig["normalization_path"]};

    // parse track data
    Track track = Track(json_paths.track_path);
    TrackPos track_xy = track.getTrack();

    // initialize mpc
    mpc = new MPC(jsonConfig["n_sqp"], jsonConfig["n_reset"], jsonConfig["sqp_mixing"], jsonConfig["Ts"], json_paths);
    mpc->setTrack(track_xy.X, track_xy.Y);
}

MPCCWrapperClass::~MPCCWrapperClass()
{
    // nothing to cleanup here
}

double* MPCCWrapperClass::calcMPC(double* state_meas)
{
    // map states to required struct
    State x0 = {
      state_meas[0], // X
      state_meas[1], // Y
      state_meas[2], // phi
      state_meas[3], // vx
      state_meas[4], // vy
      state_meas[5], // rf
      state_meas[6], // s
      state_meas[7], // D
      state_meas[8], // delta
      state_meas[9]  // vs
    };

    // solve MPC problem
    MPCReturn mpc_sol = mpc->runMPC(x0);
    // store results
    mpc_horizon = mpc_sol.mpc_horizon;

    // allocate memory for return array
    double* input_calc = new double[3];
    // map outputs to return pointer
    input_calc[0] = mpc_sol.u0.dD;
    input_calc[1] = mpc_sol.u0.dDelta;
    input_calc[2] = mpc_sol.u0.dVs;
    return input_calc;
}

double* MPCCWrapperClass::getPrediction(int idx)
{
    double* prediction = new double[N];
    for (int i = 0; i<N; i++)
    {
        if(idx == 0) {
          prediction[i] = mpc_horizon[i].xk.X;
        }
        else if(idx == 1){
          prediction[i] = mpc_horizon[i].xk.Y;
        }
        else if(idx == 2){
          prediction[i] = mpc_horizon[i].xk.phi;
        }
        else if(idx == 3){
          prediction[i] = mpc_horizon[i].xk.vx;
        }
        else if(idx == 4){
          prediction[i] = mpc_horizon[i].xk.vy;
        }
        else if(idx == 5){
          prediction[i] = mpc_horizon[i].xk.r;
        }
        else if(idx == 6){
          prediction[i] = mpc_horizon[i].xk.s;
        }
        else if(idx == 7){
          prediction[i] = mpc_horizon[i].xk.D;
        }
        else if(idx == 8){
          prediction[i] = mpc_horizon[i].xk.delta;
        }
        else if(idx == 9){
          prediction[i] = mpc_horizon[i].xk.vs;
        }
        else
        {
          prediction[i] = 0;
        }
    }
    return prediction;
}
