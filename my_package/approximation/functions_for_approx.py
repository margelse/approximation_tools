import numpy as np

# Отдельные конструкции функций

def lognormal_distribution(x, coef_peak, sigma, mu, free_term):

    '''Функция логнормального распределения с коэффициентом пика и добавочным членом.'''

    numerator = np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
    denominator = x * sigma * np.sqrt(2 * np.pi)

    lognorm_distrib = coef_peak * numerator / denominator

    return lognorm_distrib + free_term

def lognormal_distribution_exponential_with_negative_exponent(
        x, 
        coef_peak, 
        sigma, 
        mu, 
        lb, 
        free_term
):

    '''(3 умножение логнорм распредел на экспоненту с отриц показат и свободный коэфф)'''

    numerator = np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
    denominator = x * sigma * np.sqrt(2 * np.pi)
    lognorm_distrib = coef_peak * numerator / denominator

    exp_negative_exp = np.exp(-(lb * x))

    return lognorm_distrib * exp_negative_exp + free_term

def inverse_exponential(x, coef_peak, b, free_term):
    inverse_exp = coef_peak / (b + np.exp(x))

    return inverse_exp + free_term

def normal_distribution(x, coef_peak, sigma, mu, free_term):
    norm_distrib = coef_peak * (np.exp(-((x - mu)**2) / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi)))

    return norm_distrib + free_term

def inverse_power_func(x, coef_peak, b, power, free_term):
    inverse_power = coef_peak / (b + x**power)

    return inverse_power + free_term

# Кастомные функции

def lognormal_distribution_with_inverse_exponential(
        x, 
        coef_lognormal_peak, 
        sigma, 
        mu, 
        coef_inverse_exp_peak, 
        b, 
        free_term
):

    '''(8 от логнорм распредел отнимается обратная экспоненц ф-я)'''

    numerator = np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
    denominator = x * sigma * np.sqrt(2 * np.pi)
    lognorm_distrib = coef_lognormal_peak * numerator / denominator

    inverse_exp = coef_inverse_exp_peak / (b + np.exp(x))

    return lognorm_distrib + inverse_exp + free_term

def lognormal_distribution_with_normal_distrib(
        x, 
        coef_lognormal_peak, 
        sigma, 
        mu, 
        coef_norm_distrib_peak, 
        sigma2, 
        mu2,
        free_term
):

    '''(9 комбинация логнорм распредел, части норм распредел и свободного коэфф)'''

    numerator = np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
    denominator = x * sigma * np.sqrt(2 * np.pi)
    lognorm_distrib = coef_lognormal_peak * numerator / denominator

    norm_distrib = coef_norm_distrib_peak * np.exp(-(x - mu2)**2 / sigma2**2)

    return lognorm_distrib + norm_distrib + free_term

def lognormal_distribution_with_normal_distrib_and_inverse_exponential(
        x,
        coef_lognormal_peak,
        sigma,
        mu,
        coef_norm_distrib_peak,
        sigma2,
        mu2, 
        coef_inverse_exp_peak,
        b,
        free_term
):
    
    '''(10 комбинация логнорм распредел, части норм распредел, св коэфф, обр эксп ф-ии)'''

    numerator = np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
    denominator = x * sigma * np.sqrt(2 * np.pi)
    lognorm_distrib = coef_lognormal_peak * numerator / denominator

    norm_distrib = coef_norm_distrib_peak * np.exp(-(x - mu2)**2 / sigma2**2)

    inverse_exp = coef_inverse_exp_peak / (b + np.exp(x))

    return lognorm_distrib + norm_distrib - inverse_exp + free_term

def lognormal_distribution_with_inverse_power(x, coef_first_peak, sigma, mu, coef_second_peak, b, free_term, k):

    '''(4,5,6,7 от логнорм распредел отнимается обратная степенная ф-я + свободный член)'''

    numerator = coef_first_peak * np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
    denominator = x * sigma * np.sqrt(2 * np.pi)

    lognorm_distrib = numerator / denominator

    inverse_power = coef_second_peak / (b + x**k)

    return lognorm_distrib - inverse_power + free_term

def wrapper_lognormal_distribution_with_inverse_power(x, coef_first_peak, sigma, mu, coef_second_peak, b, free_term):
    return lognormal_distribution_with_inverse_power(x, coef_first_peak, sigma, mu, coef_second_peak, b, free_term, k)