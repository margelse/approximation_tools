from typing import List
import matplotlib.pyplot as plt
from ..data_structurs.base import Mapping
from ..data_structurs.approximation import ResultsApproximatingFunction


class VisualizationPlots:
    def __init__(
            self,
            figsize:tuple,
            title_figure:str=None,
            grid_visible:bool=False
    ):
        self.figsize = figsize
        self.title = title_figure
        self.grid_visible = grid_visible
    
    def _add_parametres_plot(self, ax):
        ax.grid(visible=self.grid_visible)
        ax.set_title(self.title)
        ax.legend()

    def create_plot_mapping(self, mappings:List[Mapping], labels:List[str]):
        x_list = []
        y_list = []
        for mapp in mappings:
            x_list.append(mapp.get_x())
            y_list.append(mapp.get_y())

        return self.create_plot(x_list, y_list, labels)

    def create_plot_result_approx(
            self, 
            structure_result_approx:ResultsApproximatingFunction, 
            labels:List[str]
    ):
        mappings_from_result = [
            structure_result_approx.mapping_start,
            structure_result_approx.mapping_result
        ]

        return self.create_plot_mapping(mappings_from_result, labels)

    def create_plot(self, x:List, y:List, labels:List[str]):
        fig, ax = plt.subplots(figsize=self.figsize)

        for independent_var, line, name in zip(x, y, labels):
            ax.plot(independent_var, line, label=name)

        self._add_parametres_plot(ax)
        plt.show()

        return fig