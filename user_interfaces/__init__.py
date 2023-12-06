from abc import ABC, abstractmethod
from gui import gui


class UI(ABC):
    """ Top level UI interface"""

    @abstractmethod
    def edit(self, title: str, a_dict, lookup, **kwargs) -> (bool, dict):
        pass

    def home(self, config_as_dict) -> (bool, dict):
        pass


class GraphicalUi(UI, ABC):
    """ Graphical PySimpleGUI """

    def edit(self, title: str, data_in, lookup, **kwargs) -> (bool, dict):
        if isinstance(data_in, list):
            return gui.edit_table_window(title=title, list_in=data_in, lookup=lookup, **kwargs)
        elif isinstance(data_in, dict):
            return gui.edit_item_window(title=title, dict_in=data_in, lookup=lookup, **kwargs)

    def home(self, config_as_dict: dict) -> (bool, dict):
        if not isinstance(config_as_dict, dict):
            print('can only take dict')
            exit(1)
        return gui.home(config_as_dict)

class TextUi(UI, ABC):
    """ Graphical PySimpleGUI """

    def edit(self, title: str, a_dict, lookup, **kwargs) -> (bool, dict):
        # return None
        pass

    def home(self, config_as_dict) -> (bool, dict):
        pass

def new_ui(ui_type: str = 'gui') -> UI:
    if ui_type == 'gui':
        return GraphicalUi()


if __name__ == '__main__':
    print('UI Factory')
