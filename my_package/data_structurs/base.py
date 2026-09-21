import numpy as np

class Mapping:
    def __init__(
            self,
            independent_var,
            dependent_var,
            condition_normalize:bool
    ):
        self.independent_var = independent_var
        self.dependent_var = dependent_var
        self.condition_normalize = condition_normalize

        self.shape = (len(independent_var), len(dependent_var))

    def __len__(self):
        return len(self.independent_var)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return Mapping(
                [self.independent_var[i] for i in range(start, stop, step)],
                [self.dependent_var[i] for i in range(start, stop, step)],
                self.condition_normalize
            )
        
        else:
            return (self.independent_var[key], self.dependent_var[key])

    def get_x(self):
        return np.copy(self.independent_var)
    
    def get_y(self):
        return np.copy(self.dependent_var)
    
    def get_x_value_from_idx(self, idx):
        return self.independent_var[idx]
    
    def get_y_value_from_idx(self, idx):
        return self.dependent_var[idx]
    
    def insert_point(self, point:tuple, idx:int=0):
        self.independent_var = np.insert(self.independent_var, idx, point[0])
        self.dependent_var = np.insert(self.dependent_var, idx, point[1])

