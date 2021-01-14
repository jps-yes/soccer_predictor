from scipy.io import loadmat
import numpy as np


# loads relevant MATLAB workspace variables (model was trained in MATLAB)
def load_model(file_name):
    model = loadmat(file_name)
    nn_params = model['NNparams']
    x_test = model['Xtest']
    x_cv = model['Xcv']
    input_layer_size = int(model['inputLayerSize'])
    hidden_layers_size = model['hiddenLayersSize'].astype(int)
    num_labels = int(model['numLabels'])
    mu_nn = model['mu_nn']
    sigma_nn = model['sigma_nn']
    mu_nn = mu_nn.flatten()
    sigma_nn = sigma_nn.flatten()
    mu = np.concatenate((model['mu'], np.zeros((1, 38))), axis=1)
    sigma = np.concatenate((model['sigma'][:, 0:24], np.ones((1, 38))*1/sum(x_test[1, 24:61])), axis=1)
    return nn_params, x_test, x_cv, input_layer_size, hidden_layers_size, num_labels, mu_nn, sigma_nn, mu, sigma


# reshapes array nn_params into matrices theta and arrays gamma and beta
def parameter_reshape(layers, nn_params):
    theta = [0] * (layers.size - 1)
    gamma = [0] * layers.size
    beta = [0] * layers.size
    for i in range(0, layers.size - 1):
        theta[i] = np.reshape(nn_params[0:layers[i+1] * layers[i]], (layers[i+1], layers[i]), order="F")
        nn_params = nn_params[layers[i+1] * layers[i]:]
    for i in range(0, layers.size - 1):
        gamma[i+1] = nn_params[0:layers[i+1]]
        nn_params = nn_params[layers[i+1]:]
    for i in range(0, layers.size - 1):
        beta[i+1] = nn_params[0:layers[i+1]]
        nn_params = nn_params[layers[i+1]:]
    return theta, gamma, beta


def softmax(z):
    g = np.exp(z)
    total = g.sum(axis=1)
    for i in range(0, g.shape[1]):
        g[:, i] = g[:, i] / total
    return g


# forward propagation with ReLu and softmax for output layer
def forward_propagation(layers, x, theta, mu, sigma, gamma, beta):
    a = [0] * layers.size
    a[0] = x
    z = [0] * layers.size
    z_norm = [0] * layers.size
    z_mu = [0] * layers.size
    for i in range(0, layers.size - 1):
        # MULTIPLIES WEIGHTS
        z[i + 1] = a[i].dot(theta[i].T)
        # BATCH NORMALIZATION
        z_mu[i + 1] = z[i + 1] - mu[i + 1]
        z_norm[i + 1] = z_mu[i + 1] / np.sqrt(sigma[i + 1] + 10 ** (-8))
        z[i + 1] = gamma[i + 1].T * z_norm[i + 1] + beta[i + 1].T
        # ACTIVATION FUNCTION
        if i == layers.size - 2:
            # IF IT IS THE LAST LAYER, APPLIES SOFTMAX
            a[i + 1] = softmax(z[i + 1])
        else:
            # IN OTHER LAYERS APPLIES ReLu
            a[i + 1] = np.maximum(0.01 * z[i + 1], z[i + 1])
    return a[-1]
