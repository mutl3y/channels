from abc import ABC, abstractmethod
import gui


class UI(ABC):
    """ Top level UI interface"""

    @abstractmethod
    def edit(self, title: str, a_dict, **kwargs) -> (bool, dict):
        pass


class GraphicalUi(UI, ABC):
    """ Graphical PySimpleGUI """

    def edit(self, title: str, a_dict, **kwargs) -> (bool, dict):
        if isinstance(a_dict[0], list):
            return gui.edit_table_window(title=title, a_dict=a_dict, **kwargs)
        return gui.edit_item_window(title=title, a_dict=a_dict[0], **kwargs)


class TextUi(UI, ABC):
    """ Graphical PySimpleGUI """

    def edit(self, title: str, a_dict, **kwargs) -> (bool, dict):
        # return None
        pass

def new_ui(ui_type: str = 'gui') -> UI:
    if ui_type == 'gui':
        return GraphicalUi()


if __name__ == '__main__':
    print('UI Factory')
