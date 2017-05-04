import numpy as np
import matplotlib.pyplot as plt

from gmm import GMM

if __name__ == '__main__':
    group_a = np.random.normal(loc=20.00, scale=4.0, size=1000)
    group_b = np.random.normal(loc=15.00, scale=2.0, size=1000)
    group_c = np.random.normal(loc=30.00, scale=2.0, size=1000)
    group_d = np.random.normal(loc=25.00, scale=7.0, size=1000)
    print group_a
    data = np.concatenate((group_a, group_b, group_c, group_d))

    g = GMM(n_components=4)
    eval_train = g.train(data)
    for c in g.components:
        print '*****'
        print c.mean
        print c.cov

    plt.plot(eval_train)
    plt.show()