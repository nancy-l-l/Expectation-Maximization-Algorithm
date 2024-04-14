# Expectation-Maximization-Algorithm
The expectation-maximization algorithm can be used to handle situations where variables are partially observable. When certain variables are observable, we can use those instances to learn and estimate their values. Then, we can predict the values of these variables in instances when it is not observable. 

In the E step, the algorithm computes the latent variables i.e. expectation of the log-likelihood using the current parameter estimates. 

In the M step, the algorithm determines the parameters that maximize the expected log-likelihood obtained in the E step, and corresponding model parameters are updated based on the estimated latent variables. 

In my Algorithm, I generate raw data points around a circle with noise. I iteratively repeat the E and M steps until the values converge. I then graph my generated raw data, true signal, and the EM prediction to compare.
