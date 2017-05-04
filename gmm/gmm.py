import numpy as np


class NormalDistribution:
    def __init__(self, weight, mean, cov):
        self.weight = weight
        self.mean = mean
        self.cov = cov
        self.xi = 0
        self.wpdf = []
        self.gammas = []

    def compute_pdf(self, data):
        m, n = np.shape(data)
        prec = np.linalg.inv(self.cov)
        sign, logdet = np.linalg.slogdet(prec)
        log_p_x_c = np.divide(logdet, 2.) \
                    - np.divide(np.dot(np.dot((data - self.mean), prec), (data - self.mean)), 2.) \
                    - np.multiply(np.log(2*np.pi), n/2.)
        if np.shape(log_p_x_c) == (1, 1):
            return np.exp(log_p_x_c[0, 0])
        return np.exp(log_p_x_c)

    def compute_vectorized_pdf(self, data):
        m, n = np.shape(data)
        prec = np.linalg.inv(self.cov)
        sign, logdet = np.linalg.slogdet(prec)
        log_p_x_c = np.divide(logdet, 2.) \
                    - np.divide(np.sum(np.multiply(np.dot((data - self.mean), prec), (data-self.mean)), axis=1), 2.) \
                    - np.multiply(np.log(2*np.pi), n/2.)
        return np.exp(log_p_x_c)


class GMM:
    def __init__(self, n_components=2, train_thres=0.01, max_iter=100):
        self.n_components = n_components
        self.train_thres = train_thres
        self.max_iter = max_iter
        self.components = []

    def _split_components(self):
        new_components = []
        for c in self.components:
            u, s, v = np.linalg.svd(c.cov)
            new_components.append(NormalDistribution(c.weight/2., c.mean + (u[:, 0] * np.sqrt(s[0]) * 1.), c.cov))
            new_components.append(NormalDistribution(c.weight/2., c.mean - (u[:, 0] * np.sqrt(s[0]) * 1.), c.cov))
        self.components = new_components

    def _init_components(self, data):
        mean_ext = np.mean(data, axis=0)
        cov_ext = np.dot(np.transpose(data-mean_ext), (data-mean_ext))/len(data)
        self.components.append(NormalDistribution(1, mean_ext, cov_ext))

    def train(self, data):
        self._init_components(data)

        if self.n_components == 1:
            return
        else:
            self._split_components()

        for train_iter in xrange(self.max_iter):
            if train_iter == 0:
                eval_train = []
            elif train_iter > 1 and len(eval_train) > 2 and eval_train[len(eval_train)-1] - eval_train[len(eval_train)-2] < self.train_thres:
                if len(self.components) < self.n_components:
                    print '*** split components ***'
                    self._split_components()
                    eval_train = []
                else:
                    break

            for c in self.components:
                c.wpdf = np.multiply(c.weight, c.compute_vectorized_pdf(data))

            gamma_denoms = np.zeros(len(data))
            for c in self.components:
                gamma_denoms += c.wpdf

            eval_train.append(sum(np.log(gamma_denoms)))

            for c in self.components:
                c.gammas = np.divide(c.wpdf, gamma_denoms)

            for c, i in zip(self.components, range(len(self.components))):
                c.xi = sum(c.gammas)
                mi_xk = np.dot(c.gammas, data)
                mi_xk = np.divide(mi_xk, c.xi)
                sigma_xk = np.dot(np.dot(np.transpose(data-mi_xk), np.diag(c.gammas)), (data-mi_xk))
                sigma_xk = np.divide(sigma_xk, c.xi)
                c.mean = mi_xk
                c.cov = sigma_xk

            denom_weight = 0
            for c in self.components:
                denom_weight += c.xi
            for c in self.components:
                c.weight = np.divide(c.xi, denom_weight)

            print train_iter

        return eval_train