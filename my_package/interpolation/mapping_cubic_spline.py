from ..data_structurs import Mapping
from scipy.interpolate import CubicSpline, UnivariateSpline
import numpy as np

class Interpolation:
    def __init__(self, mapping:Mapping, multiplication_coeff_count_points:int):
        self.mapping = mapping
        self.multiplication_coeff_count_points = multiplication_coeff_count_points
        self._init_mapping_params()

    def _init_mapping_params(self):
        self.x = (self.mapping).get_x()
        self.y = (self.mapping).get_y()
        self.condition_normalize = (self.mapping).condition_normalize

    def cubic_spline(self):
        x_augument = self._augment_number_partitions()
        f_cubic = CubicSpline(self.x, self.y, bc_type='natural')
        y_interpolation = f_cubic(x_augument)

        mapping_result = Mapping(
            x_augument,
            y_interpolation,
            self.condition_normalize
        )

        return mapping_result
    
    def b_spline(self, k:int, s):
        x_augument = self._augment_number_partitions()
        fb_spline = UnivariateSpline(self.x, self.y, k=k, s=s)
        y_interpolation = fb_spline(x_augument)

        mapping_result = Mapping(
            x_augument,
            y_interpolation,
            self.condition_normalize
        )

        return mapping_result

    def _augment_number_partitions(self):
        x_first, x_last = self._get_start_and_last_points()
        step = self._calculation_step()
        new_x = np.arange(x_first, x_last, step)
        
        return new_x

    def _get_start_and_last_points(self):
        return self.x[0], self.x[-1]

    def _calculation_step(self):
        return (np.abs(self.x[1] - self.x[0])) / self.multiplication_coeff_count_points