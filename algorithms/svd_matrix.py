import numpy as np

class SVD:
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.m, self.n = matrix.shape
        self.u = None
        self.sigma = None
        self.vt = None

    @staticmethod
    def compute_eigen(matrix):
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        return eigenvalues, eigenvectors

    def compute_svd(self):
        at_a = self.matrix.T @ self.matrix
        a_at = self.matrix @ self.matrix.T

        eigenvalues_v, eigenvectors_v = self.compute_eigen(at_a)
        singular_values = np.sqrt(np.maximum(eigenvalues_v, 0))

        self.sigma = np.zeros((self.m, self.n))
        for i in range(min(self.m, self.n)):
            self.sigma[i, i] = singular_values[i]

        eigenvalues_u, eigenvectors_u = self.compute_eigen(a_at)
        self.u = eigenvectors_u

        for i in range(self.u.shape[1]):
            reconstructed_column = self.matrix @ eigenvectors_v[:, i]
            if np.dot(reconstructed_column, self.u[:, i]) < 0:
                self.u[:, i] *= -1

        self.vt = eigenvectors_v.T

    def get_matrices(self):
        if self.u is None or self.sigma is None or self.vt is None:
            raise ValueError("SVD не було обчислено. Використовуйте compute_svd() спочатку.")
        return self.u, self.sigma, self.vt

    def reconstruct_matrix(self):
        if self.u is None or self.sigma is None or self.vt is None:
            raise ValueError("SVD не було обчислено. Використовуйте compute_svd() спочатку.")
        return self.u @ self.sigma @ self.vt


if __name__ == "__main__":
    A = np.array([[3, 1, 2], [1, 3, 2]])

    svd_solver = SVD(A)
    svd_solver.compute_svd()

    U, S, VT = svd_solver.get_matrices()
    print("Матриця U:\n", U)
    print("Матриця Σ:\n", S)
    print("Матриця V^T:\n", VT)

    reconstructed_A = svd_solver.reconstruct_matrix()
    print("Відновлена матриця A:\n", reconstructed_A)
