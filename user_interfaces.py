from abc import ABC, abstractmethod
import gui


class UI(ABC):
    """ Top level UI interface"""

    @abstractmethod
    def edit(self, a_dict, **kwargs) -> (bool, dict):
        pass


class GraphicalUi(UI, ABC):
    """ Graphical PySimpleGUI """

    def edit(self, a_dict, **kwargs) -> (bool, dict):
        return gui.edit_channels(a_dict=a_dict, **kwargs)


class TextUi(UI, ABC):
    """ Graphical PySimpleGUI """

    def edit(self, a_dict, **kwargs) -> (bool, dict):
        # return None
        pass

def new_ui(ui_type: str = 'gui') -> UI:
    if ui_type == 'gui':
        return GraphicalUi()


if __name__ == '__main__':
    print('UI Factory')
