from typing import List, Tuple, Callable
from ..data_structurs.base import Mapping
import pandas as pd

class StructurePipelineApproximation:
    def __init__(
            self,
            names_node:List[str],
            functions: List[Callable],
            values_sections:List[List],
            values_parametres:List[Tuple],
            bounds:List[Tuple[List]]
    ):
        self.names_node = names_node

        self.functions = functions
        self.values_sections = values_sections
        self.values_parametres = values_parametres
        self.bounds = bounds

        self._check_size()

    def _check_size(self):
        if len(self.names_node) != len(self.values_sections) & len(self.names_node) != len(self.values_parametres) & len(self.names_node) != len(self.functions):
            raise(ValueError('The size of the input data is different'))
        
    def get_pipeline(self):
        new_pipeline = dict()
        for name, func, section, parametres, bound in zip(self.names_node, self.functions, self.values_sections, self.values_parametres, self.bounds):
            new_pipeline[name] = {
                'function': func,
                'section': section,
                'parametres': parametres,
                'bounds': bound
            }

        return new_pipeline
    
class ResultsApproximatingFunction:
    def __init__(
            self,
            mapping_start:Mapping,
            mapping_result:Mapping,
            function_approximation: Callable,
            parametres_function: tuple,
            bounds_parametres: Tuple[List]
    ):
        self.mapping_start = mapping_start
        self.mapping_result = mapping_result

        self.func = function_approximation
        self.FUNCTION_NAME = self.func.__code__.co_name
        self.params = parametres_function
        self.bounds_parametres = bounds_parametres

    def metrix_values_show(self, function_metrics:dict):
        self._message_about_condition_normalize()
        self._calculation_metrix(function_metrics)

        df = self._converting_the_results_to_df(self.result_calculate)

        return df
    
    def _calculation_metrix(self, function_metrics:dict):
        self.result_calculate = [
            {name: func_metrix((self.mapping_start).get_y(), (self.mapping_result).get_y()) for name, func_metrix in function_metrics.items()}
        ]

    def _message_about_condition_normalize(self):
        print(f'Condition normalize = {self.mapping_result.condition_normalize}')

    def parametres_show(self):
        name_args = self._get_name_parametres_from_function()
        names_and_values = self._filling_dict(name_args, self.params)

        df = self._converting_the_results_to_df(names_and_values)

        return df
    
    def bounds_parametres_show(self):
        name_args = self._get_name_parametres_from_function()
        bounds_for_separate_params = self._get_bounds_for_separate_params()
        names_and_values = self._filling_dict(name_args, bounds_for_separate_params)

        df = self._converting_the_results_to_df(names_and_values)

        return df
    
    def _get_bounds_for_separate_params(self):
        bounds = []
        for inf, sup in zip(*self.bounds_parametres):
            bounds.append((inf, sup))

        return bounds

    def _get_name_parametres_from_function(self):
        all_name_args = (self.func).__code__.co_varnames
        number_start_args = 1
        count_args = (self.func).__code__.co_argcount
        name_args = all_name_args[number_start_args:count_args]

        return name_args
    
    def _filling_dict(self, keys, values):
        result = [
            {key: val for key, val in zip(keys, values)}
        ]

        return result

    def _converting_the_results_to_df(self, list_with_dict):
        return pd.DataFrame(list_with_dict)