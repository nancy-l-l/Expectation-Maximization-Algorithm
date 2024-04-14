import numpy as np
import matplotlib.pyplot as plt

# Function to generate raw data points around a circle with noise
def generate_data(radius, num_points, noise_std):
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = radius * np.cos(theta) + np.random.normal(0, noise_std, num_points)
    y = radius * np.sin(theta) + np.random.normal(0, noise_std, num_points)
    #returns num_points number of (x, y) arrays with a normal distribution + noise in shape of circle
    return np.vstack((x, y)).T


# Function to initialize parameters
def initialize_parameters(num_clusters, data):
    # data dimensions = #points arrays * #dimensions elements in each array
    num_points, num_dimensions = data.shape

    #returns sample from std normal dist
    mean = np.random.randn(num_clusters, num_dimensions) * np.std(data, axis=0)

    #create an array of 0's of dimensions*clusters, data type = num_dimensions
    covariance = np.zeros((num_clusters, num_dimensions, num_dimensions))
    for i in range(num_clusters):
        #every element of covariance is sqr 2-D array of size num_dimensions with diagonal 1's and 0's elsewhere.
        covariance[i] = np.eye(num_dimensions)

        #weight = array of num_clusters filled w ones / size
    weight = np.ones(num_clusters) / num_clusters
    return mean, covariance, weight


# E-step: Update responsibilities
def expectation(data, mean, covariance, weight):
    #data = (x,y) of all data points
    #mean = random sample of (x,y) pts
    #covariance: check if the covariance passed is in fact a covariance
    num_points = data.shape[0]
    num_clusters = len(mean)
    # responsibilities = Return a new array of given shape filled with zeros
    responsibilities = np.zeros((num_points, num_clusters))

    for k in range(num_clusters):
        diff = data - mean[k]
        #np.linalg.inv(covariance[k]) returns inverse of covariance[k]
        #np.dot(a,b) (a = tuple) so it is a sum product over the last axis of a and the second-to-last axis of b = sum(a[i,j,:] * b[k,:,m])
        #exponet =  computes log likelihood of each data point generated by k-th Gaussian component. calculates the Mahalanobis distance for each data point from mean of distribution (covariance matrix).
        exponent = -0.5 * np.sum(np.dot(diff, np.linalg.inv(covariance[k])) * diff, axis=1)
        #first : = rows, second : = columns
        responsibilities[:, k] = weight[k] * np.exp(exponent)

    responsibilities /= np.sum(responsibilities, axis=1, keepdims=True)
    return responsibilities


# Maximization-step: Update parameters
def maximization(data, responsibilities):
    num_clusters = responsibilities.shape[1]
    num_points, num_dimensions = data.shape

    Nk = np.sum(responsibilities, axis=0)
    mean = np.dot(responsibilities.T, data) / Nk[:, None]

    covariance = np.zeros((num_clusters, num_dimensions, num_dimensions))
    for k in range(num_clusters):
        # Update covariances
        diff = data - mean[k]
        covariance[k] = np.dot(responsibilities[:, k] * diff.T, diff) / Nk[k]

    # Update weights
    weight = Nk / num_points

    return mean, covariance, weight


# MAIN EM algorithm implementation
def EM_algorithm(data, num_clusters, max_iterations=100, tolerance=1e-3):

    #initialize values
    mean, covariance, weight = initialize_parameters(num_clusters, data)

    #sets max num of iterations incase no convergence
    for iteration in range(max_iterations):
        #sets old to test against new
        old_mean, old_covariance, old_weight = mean.copy(), covariance.copy(), weight.copy()

        #expectation
        responsibilities = expectation(data, mean, covariance, weight)
        #maximization
        mean, covariance, weight = maximization(data, responsibilities)

        mean_change = np.mean(np.abs(mean - old_mean))
        covariance_change = np.mean(np.abs(covariance - old_covariance))
        weight_change = np.mean(np.abs(weight - old_weight))

        if mean_change < tolerance and covariance_change < tolerance and weight_change < tolerance:
            break

    return mean, covariance, weight


def user_input(radius, num_points, noise_std):
    # Generate raw data points around a circle with noise
    raw_data = generate_data(radius, num_points, noise_std)

    # Define true parameters (for comparison)
    true_mean = np.array([[radius, 0], [0, radius]])
    true_covariance = np.array([[[noise_std ** 2, 0], [0, noise_std ** 2]], [[noise_std ** 2, 0], [0, noise_std ** 2]]])
    true_weight = np.array([0.5, 0.5])

    # Plot raw data
    plt.figure(figsize=(8, 6))
    plt.scatter(raw_data[:, 0], raw_data[:, 1], color='b', s=4, label='Raw Data')

    # Plot true signal
    theta = np.linspace(0, 2 * np.pi, 100)
    true_circle_x = radius * np.cos(theta)
    true_circle_y = radius * np.sin(theta)
    plt.plot(true_circle_x, true_circle_y, color='r', linestyle='--', label='True Signal')

    # Implement EM algorithm
    num_clusters = 2
    estimated_mean, estimated_covariance, estimated_weight = EM_algorithm(raw_data, num_clusters)

    # Plot EM prediction
    for i in range(num_clusters):
        estimated_circle_x = estimated_mean[i, 0] + 1.5*np.sqrt(estimated_covariance[i, 0, 0]) * np.cos(theta)
        estimated_circle_y = estimated_mean[i, 1] + 1.5*np.sqrt(estimated_covariance[i, 1, 1]) * np.sin(theta)
        plt.plot(estimated_circle_x, estimated_circle_y, color='g', linestyle='-', label='EM Prediction')

user_input( 2, 1000, .3)

plt.title('EM Algorithm for Gaussian Mixture Model')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.axis('equal')
plt.show()
