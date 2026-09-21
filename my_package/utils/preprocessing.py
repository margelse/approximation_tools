import numpy as np
from ..data_structurs.base import Mapping
from ..data_structurs.approximation import ResultsApproximatingFunction

class MinMaxNormalize:
    def __init__(self, values_start):
        self.values_start = values_start
        
        self.max_value = np.max(self.values_start)
        self.min_value = np.min(self.values_start)

    def normalize(self):
        values_normalize = (self.values_start - self.min_value) / (self.max_value - self.min_value)
        
        return values_normalize
    
    def denormalize(self, values_normalize):
        return values_normalize * (self.max_value - self.min_value) + self.min_value
    
class MinMaxNormalizeForMappings:
    def __init__(self, mapping:Mapping|list):
        self.mapping = mapping
        self._init_minmax_values()

    def _init_minmax_values(self):
        self.max_value = np.max((self.mapping).get_y())
        self.min_value = np.min((self.mapping).get_y())

    def normalize(self):
        if not self.mapping.condition_normalize:
            dependent_v = (self.mapping).get_y()
            dependent_normalize_v = (dependent_v - self.min_value) / (self.max_value - self.min_value)

            return Mapping((self.mapping).get_x(), dependent_normalize_v, True)
        
        else:
            raise(ValueError('The mapping is already normalized!'))
        
    def denormalize(self, mapping_normalize:Mapping):
        if mapping_normalize.condition_normalize:
            dependent_denormalize_v = mapping_normalize.get_y() * (self.max_value - self.min_value) + self.min_value

            return Mapping(mapping_normalize.get_x(), dependent_denormalize_v, False)
        
        else:
            raise(ValueError('The mapping was not normalized!'))
        
def denormalize_result_approx_struct(
        result_approx:ResultsApproximatingFunction,
        start_mapping_normalize_obj:MinMaxNormalizeForMappings
):
    denormalize_result = ResultsApproximatingFunction(
        start_mapping_normalize_obj.denormalize(result_approx.mapping_start),
        start_mapping_normalize_obj.denormalize(result_approx.mapping_result),
        result_approx.func,
        result_approx.params,
        result_approx.bounds_parametres
    )
    return denormalize_result 
    
class MappingPreprocessingForApproximation:
    def __init__(self, mapping:Mapping):
        self.mapping = mapping
        self._init_mapping_attributes()

    def _init_mapping_attributes(self):
        self.x = (self.mapping).get_x()
        self.y = (self.mapping).get_y()
        self.condition_normalize = (self.mapping).condition_normalize
    
    def check_none(self):
        for name, val in zip(['x', 'y'], (self.x, self.y)):
            count_none = np.sum(np.isnan(val))
            if count_none > 0:
                self._print_message_if_none
                return True
        
        return False
    
    def _print_message_if_none(self, values):
        print(f'{values} contains nan')

    def retreat_from_zero(self):
        X_without_zero = np.copy(self.x)
        X_without_zero[X_without_zero == 0] = 1e-4

        return X_without_zero
    
def get_informative_slice(mapping:Mapping, percent:float):
    count_points = len(mapping.get_x())
    informative_count_points = int(count_points * percent)

    informative_slice_mapping = Mapping(
        mapping.get_x()[0:informative_count_points].copy(),
        mapping.get_y()[0:informative_count_points].copy(),
        mapping.condition_normalize
    )

    other_mapping = Mapping(
        mapping.get_x()[informative_count_points - 1:-1].copy(),
        mapping.get_y()[informative_count_points - 1:-1].copy(),
        mapping.condition_normalize
    )

    return informative_slice_mapping, other_mapping

def get_idx_extreme_points(mapping:Mapping, size_window:int):
    directions = _get_directions_for_mapping(mapping, size_window)
    extreme_idx = []

    for idx in range(len(directions) - 1):
        if directions[idx] * directions[idx + 1] < 0:
            extreme_idx.append((idx + 1) * size_window)

    return extreme_idx

def _get_directions_for_mapping(mapping:Mapping, size_window:int):
    y = mapping.get_y()
    directions = []

    for idx in range(0, len(y), size_window):
        if len(y) - idx < size_window:
            break

        derivative = np.diff(y[idx:idx + size_window])
        directions.append(np.mean(derivative))

    return directions

# --------------- Первый способ разбиения - на выходе непрерывные значения параметров ---------------

def loader_values_border_continuous_parts(mapping:Mapping, extreme_points_idx:list, count_parts:int):
    nodes_for_approximation = _create_nodes_for_parts(mapping, extreme_points_idx, count_parts)

    for section_dix in range(0, len(nodes_for_approximation) - 1, 2):
        parts = []
        for idx_start, idx_end in zip(nodes_for_approximation[section_dix], nodes_for_approximation[section_dix + 1]):
            parts.append([mapping.get_x_value_from_idx(idx_start), mapping.get_x_value_from_idx(idx_end)])

        yield parts

def _create_nodes_for_parts(mapping:Mapping, extreme_points_idx:list, count_parts:int):
    sections = _slice_mapping_on_sections(mapping, extreme_points_idx)
    count_sections = len(sections)

    all_nodes_for_parts = []

    for i, section in enumerate(sections):
        local_parts_nodes = []

        if i == (count_sections - 1):
            local_parts_nodes.extend(_calculate_nodes_for_section(section, count_parts))
            right_border = section[1]
            local_parts_nodes.append(right_border)
            all_nodes_for_parts.append(local_parts_nodes)

            break

        if i % 2 == 0:
            left_border = section[0]
            local_parts_nodes.append(left_border)
            local_parts_nodes.extend(_calculate_nodes_for_section(section, count_parts))

        else:
            local_parts_nodes.extend(_calculate_nodes_for_section(section, count_parts))
            right_border = section[1]
            local_parts_nodes.append(right_border)
        
        all_nodes_for_parts.append(local_parts_nodes)

    return all_nodes_for_parts

def _slice_mapping_on_sections(mapping:Mapping, extreme_points_idx:list)->list:
    START_IDX = 0

    nodes = [START_IDX]
    nodes.extend(extreme_points_idx)
    last_idx = mapping.shape[0] - 1
    nodes.append(last_idx)

    sections = []

    for idx in range(len(nodes) - 1):
        sections.append([nodes[idx], nodes[idx + 1]])

    return sections

def _calculate_nodes_for_section(section:list, count_parts:int):
    COUNT_BASE_NODE_IN_SECTION = 1

    local_parts_nodes = []

    count_points_section = _calculate_count_points_for_section(section)
    step_node = count_points_section // count_parts

    left_border = section[0]
    for count in range(COUNT_BASE_NODE_IN_SECTION, count_parts):
        local_parts_nodes.append(left_border + count * step_node)

    return local_parts_nodes

def _calculate_count_points_for_section(idx_borders_section:list):
    return idx_borders_section[1] - idx_borders_section[0]

# --------------- Второй способ разбиения - на выходе отрезки с точками экстремума для аппроксимации ---------------

def get_values_border_picewise_parts(mapping:Mapping, extreme_points_idx:list, margin_ratio:float):
    borders_parts = _create_borders_for_parts(mapping, extreme_points_idx, margin_ratio)

    parts_for_approximation = []

    for idx_borders_part in borders_parts:
        value_left_border = mapping.get_x_value_from_idx(idx_borders_part[0])
        value_right_border = mapping.get_x_value_from_idx(idx_borders_part[1])

        parts_for_approximation.append([value_left_border, value_right_border])

    return parts_for_approximation

def _create_borders_for_parts(mapping:Mapping, extreme_points_idx:list, margin_ratio:float):
    sections = _slice_mapping_on_sections(mapping, extreme_points_idx)
    count_sections = len(sections)

    all_nodes_for_parts = []
    left_border_part = sections[0][0]
    right_border_part = 0

    for section_idx in range(1, count_sections):
        right_border_part = sections[section_idx][0] + int(_calculate_count_points_for_section(sections[section_idx]) * margin_ratio)

        if section_idx == count_sections - 1:
            right_border_part = sections[section_idx][1]

        all_nodes_for_parts.append([left_border_part, right_border_part])

        left_border_part = right_border_part

    return all_nodes_for_parts

# def _create_borders_for_parts(mapping:Mapping, extreme_points_idx:list, margin_ratio:float):
#     sections = _slice_mapping_on_sections(mapping, extreme_points_idx)
#     count_sections = len(sections)

#     all_nodes_for_parts = []

#     for section_idx in range(0, count_sections - 1):
#         left_border_part = sections[section_idx][0]
#         right_border_part = int(sections[section_idx + 1][1] * margin_ratio)

#         all_nodes_for_parts.append([left_border_part, right_border_part])

#     return all_nodes_for_parts