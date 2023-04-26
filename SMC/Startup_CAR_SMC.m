%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Parameters 
CS_PID_y0    = 0;
CS_PID_yd0   = 0;
CS_PID_psi0  = 0;
CS_PID_psid0 = 0;

PRERL_SMC_delta_0 = 0.98;
PRERL_SMC_k  = 1000000;
PRERL_SMC_alpha = 0.01;
PRERL_SMC_p = 0.01;
PRERL_SMC_lambda = 0.1;
PRERL_SMC_beta = 0.15;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Calpha_f = 100000;
m = 2325;
Iz = 4132;
lf = 2;

Ctrl_Couple =  (2*lf*Calpha_f)/Iz;


