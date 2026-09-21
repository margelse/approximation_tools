import os

# TODO
# разделить входные параметры CSVFilesObject на 2 класса: 1 - инфа про файлы (разделитель, расширение и тд), 2 - инфа про данные (нормализованные и тд)


class CSVFilesObject:
    def __init__(
            self,
            directory:str,
            separation:str,
            condition_normalize_dependent_values:bool
    ):
        self.directory = rf'{directory}'
        self.separation = separation
        self.condition_normalize_dependent_values = condition_normalize_dependent_values

        self._init_sorted_files()

    def _init_sorted_files(self):
        all_file_paths = self._get_file_paths()
        self.valid_file_paths, self.delete_files = self._search_not_csv_files(all_file_paths)

    def _get_file_paths(self):
        files_from_dir = sorted(os.listdir(self.directory))
        file_paths = [os.path.join(self.directory, path) for path in files_from_dir]

        return file_paths

    def _search_not_csv_files(self, all_paths):
        VALID_FORMAT = '.csv'
        delete_files = []
        valid_file_paths = []

        for path in all_paths:
            _, format_file = os.path.splitext(path)

            if format_file == VALID_FORMAT:
                valid_file_paths.append(path)

            else:
                delete_files.append(path)

        return valid_file_paths, delete_files
    
    def get_valid_paths(self):
        return (self.valid_file_paths).copy()
    
    def description(self): # Через TEMPLATE можно изменять поля класса!? Так быть не должно
        TEMPLATE = {
            'directory': self.directory,
            'sorted file paths': self.valid_file_paths,
            'delete files': self.delete_files
        }

        return TEMPLATE
