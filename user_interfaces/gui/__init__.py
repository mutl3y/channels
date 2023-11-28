#!/usr/bin/env python3

import time
from typing import Dict, Any

import PySimpleGUI


def decorate(func, ):
    def wrapper(*args, **kwargs):
        print(f'******** {func} **********************')
        for a in args:
            print(f'******** func args {a}  *****************\n')
        return func(*args, **kwargs)

    return wrapper


debug = False
theme: str = 'bluePurple'


def log(*args, sleep: int = 0):
    if debug:
        for a in args:
            print(f'***** {a} *****')
    time.sleep(sleep)


def pack(header: list, list_in: list) -> dict:
    """ takes a list of headers and values and packs into a dictionary"""
    d = dict()
    if len(header) == 1 and len(list_in) > 1:
        d[header[0]] = list_in
    else:
        i = 0
        for li in list_in:
            log(f' {li}')
            d[header[i]] = li
            i += 1
    return d


def element_size(item, multiplier: int = 1) -> tuple:
    element_length = len(str(item))
    if element_length <= 1:
        element_length += 2
    else:
        element_length *= multiplier
    return element_length, 0


def set_theme(title='Choose Theme', auto_close: int = 60):
    global theme

    # theme_chosen = None

    def _layout():
        """function to set up window"""
        layout = [
            [PySimpleGUI.Text("See how elements look under different themes by choosing a different theme here!")],
            [PySimpleGUI.Listbox(
                values=PySimpleGUI.theme_list(), size=(20, 12), key='-THEME LISTBOX-', enable_events=True)],
            [PySimpleGUI.Button(button_text="Set Theme", key='set_theme', visible=False),
             PySimpleGUI.Button(button_text='Preview', key='preview_theme')]]
        # noinspection PyTypeChecker
        window = PySimpleGUI.Window(title=title, layout=layout, keep_on_top=True,
                                    auto_close=isinstance(auto_close, int),
                                    auto_close_duration=auto_close, auto_size_text=True, auto_size_buttons=True,
                                    size=(None, None), resizable=True)

        return window

    theme_window = _layout()

    # eventloop
    while True:
        event, values = theme_window.read(timeout=100)
        if event in (None, 'Cancel', PySimpleGUI.WIN_CLOSED):
            break
        elif '-THEME LISTBOX-' in event:
            if len(values['-THEME LISTBOX-']) >= 1:
                theme_window['set_theme'].update(visible=True)
            else:
                theme_window['set_theme'].update(visible=False)
        elif "set_theme" in event:
            theme_chosen = values['-THEME LISTBOX-'][0]
            theme = str(theme_chosen)
            break
        elif "preview_theme" in event:
            PySimpleGUI.theme(values['-THEME LISTBOX-'][0])
            theme_window.close()
            theme_window: PySimpleGUI.Window = _layout()
        theme_window.refresh()
    theme_window.close()

    return


def element_picker(key, value, lookup: dict = None) -> [[PySimpleGUI.Element]]:
    font = 'Courier 22 '
    bold = font + ' bold'
    if key in lookup.keys():
        log(f'found lookup')
        lookup_values = [v for v in lookup[key]]
    else:
        log(f'did not find {key} in {lookup.keys().__str__()}')
        lookup_values = None

    if isinstance(value, bool):
        """ returns a row with item name and a toggle button """
        return [[
            PySimpleGUI.Text(text=key, auto_size_text=True, font=bold), PySimpleGUI.Push(),
            PySimpleGUI.Combo(default_value=str(value), values=[True, False], auto_size_text=True, font=font),

        ]]
    elif isinstance(value, str):
        if isinstance(lookup_values, list):
            return [[
                PySimpleGUI.Text(key, font=bold), PySimpleGUI.Push(),
                PySimpleGUI.Combo(default_value=str(value), values=lookup_values, auto_size_text=True, font=font,
                                  key=f'-COMBO-#{key}', enable_events=True)]]
        else:
            return [[
                PySimpleGUI.Text(key, font=bold), PySimpleGUI.Push(),
                PySimpleGUI.InputText(default_text=str(value), expand_x=True, expand_y=True, justification='center',
                                      font=font,
                                      size=element_size(value, 2), enable_events=True, key=f'-InputText-#{key}'), ]]
    elif isinstance(value, int):
        return [[
            PySimpleGUI.Text(key, font=bold),
            PySimpleGUI.Push(),
            PySimpleGUI.InputText(default_text=value, expand_x=True, expand_y=True, justification='center', font=font,
                                  size=element_size(value, 2), enable_events=True, change_submits=True,
                                  key=f'-AUTO_SIZE-{key}')]]

    else:
        print(f'Invalid {key}  {value}')
        return [[PySimpleGUI.Text(key), PySimpleGUI.Push(),
                 PySimpleGUI.Text(key + '  ' + str(value), expand_x=False, justification='center', expand_y=False,
                                  size=element_size(value))]]


def window_with_menu(title: str, layout: list[list[PySimpleGUI.Element]], auto_close: int = None) -> PySimpleGUI.Window:
    # print(len(layout))
    # print(theme)
    camel_case_title = title.replace(" ", "_")
    PySimpleGUI.theme(theme)
    main_menu_def = [['Settings', ['Theme::edit_theme', 'TextSize']]]
    menu = [[PySimpleGUI.Menu(menu_definition=main_menu_def, key='main_menu')]]

    combined_layout = menu
    combined_layout += layout.copy()
    combined_layout += [[PySimpleGUI.B('Ok', key=f'-OK-{camel_case_title}'),
                         PySimpleGUI.B('Cancel', key=f'-CANCEL-{camel_case_title}')]]
    combined_layout += [[PySimpleGUI.Sizegrip()]]

    # noinspection PyTypeChecker
    window = PySimpleGUI.Window(title=title, layout=combined_layout, keep_on_top=True,
                                auto_close=isinstance(auto_close, int),
                                auto_close_duration=auto_close, auto_size_text=True, auto_size_buttons=True,
                                size=(None, None), resizable=True, finalize=True)

    return window


def edit_item_window(title: str, dict_in: dict, auto_close: int = None, lookup=None) -> (bool, dict):
    camel_case_title = title.replace(" ", "_")
    print(camel_case_title)
    data_changed: bool = False

    if lookup is None:
        lookup = {}

    def _layout():
        layout = []
        for _key, item in dict_in.items():
            if isinstance(item, dict):
                log(f'child {item.keys()}')
                for k, v in item.items():
                    layout += element_picker(k, v, lookup=lookup)
            else:
                log(f'found {type(item)}')
                layout += element_picker(_key, item, lookup=lookup)

        return window_with_menu(title=title, layout=layout, auto_close=auto_close)

    window = _layout()
    selected_row: tuple

    while True:
        event, values = window.read(timeout=1000)
        # todo this is for development
        if event not in (PySimpleGUI.TIMEOUT_EVENT, PySimpleGUI.WIN_CLOSED, 'THEME'):
            log(f'============ Event = {event} ==============')
            log(values)

        if event in (None, f'-CANCEL-{camel_case_title}'):
            break
        elif isinstance(event, int):
            log(f'whoops need to assign a key {event}')
        elif '-BOOL- ' in event:
            log(f'bool {event}, {values}')
        elif 'Theme::edit_them' in event:
            set_theme()
            window.close()
            window = _layout()
        elif '-InputText-#' in event:
            key = str(event).split("#")[1]
            dict_in[key] = values[event]
            data_changed = True
            window[event].update(values[event])
        elif '-COMBO-#' in event:
            key = str(event).split("#")[1]
            dict_in[key] = values[event]
            data_changed = True
        elif f'-OK-{camel_case_title}' in event:
            log(f'Ok Pressed better save {dict_in} ')
            if data_changed:
                window.close()
                return True, dict_in

        window.refresh()

    window.close()
    return False, {}


def edit_table_window(title: str, list_in: list, auto_close: int = None, lookup=None) -> (bool, dict):
    """
    Show the channel configuration window

    # :return: True if settings were changed
    # :rtype: (bool)
    """
    camel_case_title = title.replace(" ", "_")
    if lookup is None:
        lookup = {}

    data_changed: bool = False
    if not isinstance(list_in, list):
        log(f'Well this was unexpected need list = {type(list_in)}')
        exit(1)

    headers = list(list_in[0].keys())
    data = [list(i.values()) for i in list_in]

    def _layout():
        right_click_menu_def = [[], ['Add', 'Edit ', 'Clone', 'Delete']]
        layout = [
            [PySimpleGUI.Table(values=data, headings=headers, auto_size_columns=True, display_row_numbers=False,
                               justification='center', key='-TABLE-', selected_row_colors='red on yellow',
                               enable_events=False, expand_x=True, expand_y=True, enable_click_events=True,
                               right_click_selects=True, right_click_menu=right_click_menu_def)],
        ]
        return window_with_menu(title=title, layout=layout, auto_close=auto_close)

    window = _layout()
    selected_row = tuple()

    while True:
        event, values = window.read(timeout=100)

        # event, [1,2,3] = test_events.pop(0)
        # todo this is for development
        if event not in (PySimpleGUI.TIMEOUT_EVENT, PySimpleGUI.WIN_CLOSED, 'Delete'):
            log(f'Event = {event} ')
            # print(values)
        if event in (None, f'-CANCEL-{camel_case_title}', PySimpleGUI.WIN_CLOSED):
            return False, {}
        elif '-TABLE-' and '+CLICKED+' in event:
            if len(values['-TABLE-']) > 0:
                selected_row = int(values['-TABLE-'][0])
                log(f'selected_row= {selected_row}')
            else:
                selected_row = None
        elif 'Delete' in event:
            del data[selected_row]
        elif 'Clone' in event:
            if isinstance(selected_row, int):
                data.append(data[selected_row])
        elif 'Add' in event:
            data.append(['Add', 'data', 'here'])
        elif 'Edit' in event:
            log(f'selected_row={selected_row} {type(selected_row)}')
            if selected_row is None:
                log('selected_row is type: None, Ignoring click')
                continue
            elif isinstance(selected_row, int) and selected_row >= 0:
                d = pack(header=headers, list_in=data[selected_row])
                changed, di = edit_item_window(title=d['name'], dict_in=d, auto_close=auto_close, lookup=lookup)
                if changed:
                    data[selected_row] = di
                    del di
                    data_changed = True
                    print(data)
                pass
            else:
                log(f'Uncaught edit event {data[selected_row]} =============================')

        elif event == f'-OK-{camel_case_title}':
            return data_changed, pack([title], data)
        elif 'Theme::edit_them' in event:
            set_theme()
            window.close()
            window = _layout()

        window['-TABLE-'].update(values=data)

        window.refresh()


def home(config_as_dict: dict, title: str = 'Tuning Files Helper', auto_close: int = 5):  # todo  change this auto_close to none
    """app main page"""
    camel_case_title = title.replace(" ", "_")

    def _layout():
        right_click_menu_def = [[], ['Add', 'Edit ', 'Clone', 'Delete']]
        layout = [
            [PySimpleGUI.Tree()],
            # [PySimpleGUI.Table(values=data, headings=headers, auto_size_columns=True, display_row_numbers=False,
            #                    justification='center', key='-TABLE-', selected_row_colors='red on yellow',
            #                    enable_events=False, expand_x=True, expand_y=True, enable_click_events=True,
            #                    right_click_selects=True, right_click_menu=right_click_menu_def)],
        ]
        return window_with_menu(title=title, layout=layout, auto_close=auto_close)

    window = _layout()
    selected_row = tuple()

    while True:
        event, values = window.read(timeout=100)

        # event, [1,2,3] = test_events.pop(0)
        # todo this is for development
        if event not in (PySimpleGUI.TIMEOUT_EVENT, PySimpleGUI.WIN_CLOSED, 'Delete'):
            log(f'Event = {event} ')
            # print(values)
        if event in (None, f'-CANCEL-{camel_case_title}', PySimpleGUI.WIN_CLOSED):
            return False, None
        # elif '-TABLE-' and '+CLICKED+' in event:
        #     if len(values['-TABLE-']) > 0:
        #         selected_row = int(values['-TABLE-'][0])
        #         log(f'selected_row= {selected_row}')
        #     else:
        #         selected_row = None
        # elif 'Delete' in event:
        #     del data[selected_row]
        # elif 'Clone' in event:
        #     if isinstance(selected_row, int):
        #         data.append(data[selected_row])
        # elif 'Add' in event:
        #     data.append(['Add', 'data', 'here'])
        # elif 'Edit' in event:
        #     log(f'selected_row={selected_row} {type(selected_row)}')
        #     if selected_row is None:
        #         log('selected_row is type: None, Ignoring click')
        #         continue
        #     elif isinstance(selected_row, int) and selected_row >= 0:
        #         d = pack(header=headers, list_in=data[selected_row])
        #         changed, di = edit_item_window(title=d['name'], dict_in=d, auto_close=auto_close, lookup=lookup)
        #         if changed:
        #             data[selected_row] = di
        #             del di
        #             data_changed = True
        #             print(data)
        #         pass
        #     else:
        #         log(f'Uncaught edit event {data[selected_row]} =============================')
        #
        # elif event == f'-OK-{camel_case_title}':
        #     return data_changed, pack([title], data)
        # elif 'Theme::edit_them' in event:
        #     set_theme()
        #     window.close()
        #     window = _layout()
        #
        # window['-TABLE-'].update(values=data)

        window.refresh()


    return False, None

# def edit(self, title: str, data_in, lookup, **kwargs) -> (bool, dict):
#     if isinstance(data_in, list):
#         return edit_table_window(title=title, list_in=data_in, lookup=lookup, **kwargs)
#     elif isinstance(data_in, dict):
#         return edit_item_window(title=title, dict_in=data_in, **kwargs)