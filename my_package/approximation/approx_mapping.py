from typing import List, Tuple, Callable

import numpy as np
import pandas as pd

from scipy.optimize import curve_fit
from scipy.ndimage import uniform_filter1d

from ..data_structurs.base import Mapping
from ..data_structurs.approximation import ResultsApproximatingFunction
from ..utils.preprocessing import MappingPreprocessingForApproximation
from ..utils.visualization import VisualizationPlots
from ..utils.loaders import PipelineLoader
    
# ---------------------------------------------------------------------------------------------------------------------

def preprocessing_pipeline(mapping:Mapping):
    mapping_processing_start = MappingPreprocessingForApproximation(mapping)

    if not mapping_processing_start.check_none():
        x_without_zero = mapping_processing_start.retreat_from_zero()
    else:
        raise(ValueError('There are None values'))
    
    y = mapping_processing_start.y

    mapping_result = Mapping(x_without_zero, y, mapping_processing_start.condition_normalize)

    return mapping_result

def run_pipeline(pipeline_loader:PipelineLoader):
    result = []
    for name_node, func, mapping, parametres, bounds in pipeline_loader:
        try:
            approx = search_most_viable_parametres(func, mapping, parametres, bounds)

        except Exception as e:
            print(f'ERRORS IN {name_node}!')
            raise(e)
        
        result.append(approx)

    return result

def search_most_viable_parametres(
        function_approximation:Callable,
        mapping:Mapping,
        init_parametres:tuple,
        bounds: Tuple[List]
):
    x, y, condition_normalize = _unpacking_mapping(mapping)
    
    try:
        popt, _ = curve_fit(function_approximation, x, y, method='trf', p0=init_parametres, bounds=bounds, maxfev=10000)
    except Exception as e:
        raise(e)

    y_approx = function_approximation(x, *popt)

    mapping_approx = Mapping(x, y_approx, condition_normalize)
    result = ResultsApproximatingFunction(
        mapping,
        mapping_approx,
        function_approximation,
        popt,
        bounds
    )
    return result

def _unpacking_mapping(mapping:Mapping):
    return mapping.get_x(), mapping.get_y(), mapping.condition_normalize


def get_description_about_results_approximation(
        result_approximating:ResultsApproximatingFunction
):
    print('Values MVP:')
    print(result_approximating.parametres_show())

    print('Bounds:')
    print(result_approximating.bounds_parametres_show())

def print_plots_results(
        result_approximating:ResultsApproximatingFunction,
        visualization_result:VisualizationPlots
):
    x, y, condition_normalize = _unpacking_mapping(result_approximating.mapping)
    y_approx = result_approximating.y_approx
    
    if condition_normalize:
        y_approx = result_approximating.y_approx_denormalize

    visualization_result.create_plot([x, x], [y, y_approx], ['start line', 'approx line'])

def uniform_filter1d_for_mapping(mapping:Mapping, size_window:int):
    smooth_mapping = Mapping(
        mapping.get_x(),
        uniform_filter1d(mapping.get_y(), size=size_window),
        mapping.condition_normalize
    )

    return smooth_mapping