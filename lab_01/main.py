import matplotlib.pyplot as plt
from scipy.stats import poisson
import numpy as np


def ud_function(a, b, x_arr):
    return [(x - a) / (b - a) if a <= x < b else 0 if x < a else 1 for x in x_arr]


def ud_density(a, b, x_arr):
    return [1 / (b - a) if a <= x <= b else 0 for x in x_arr]


def puasson_density(x_arr, lambda_):
    dist = poisson(lambda_)
    return dist.pmf(x_arr)


def puasson_func(x_arr, lambda_):
    dist = poisson(lambda_)
    return dist.cdf(x_arr)


def main():
    a = int(input("Input a: "))
    b = int(input("Input b: "))

    delta = b - a
    x = np.linspace(a - delta / 2, b + delta / 2, 1000)
    y_function = ud_function(a, b, x)
    y_density = ud_density(a, b, x)

    plt.subplot(221)
    plt.title('Функция равномерного распределения')
    plt.plot(x, y_function, color='r', label=r'F({0}, {1})'.format(a, b))
    plt.legend()

    plt.subplot(223)
    plt.title('Функция плотности равномерного распределения')
    plt.plot(x, y_density, color='r', label=r'f({0}, {1})'.format(a, b))
    plt.legend()

    lambda_ = int(input("Input lambda: "))
    x = np.arange(-10, 30, 1)
    y_function = puasson_func(x, lambda_)
    y_density = puasson_density(x, lambda_)

    plt.subplot(222)
    plt.title('Функция распределения Пуассона')
    plt.plot(x, y_function, color='b', label=r'F({0})'.format(lambda_))
    plt.legend()

    plt.subplot(224)
    plt.title('Функция плотности распределения Пуассона')
    plt.plot(x, y_density, color='b', label=r'f({0})'.format(lambda_))
    plt.legend()

    plt.show()


if __name__ == '__main__':
    main()
