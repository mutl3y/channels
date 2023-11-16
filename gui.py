#!/usr/bin/env python3

import PySimpleGUI as sg
import channels
import time
from persistence.data_class_storage import To_yaml as Settings


def channels_window(conf: dict, theme: str = 'bluePurple') -> (bool, dict):
    """
    Show the channel configuration window

    # :return: True if settings were changed
    # :rtype: (bool)
    """
    try:
        sg.Theme = conf.theme
    except:
        sg.Theme = theme
    selected_cell = None

    val = [list(i.values()) for i in conf.channels]
    headers = [header.capitalize() for header in conf.channels[0].keys()]

    right_click_menu_def = [[], ['Add', 'Edit ', 'Clone', 'Delete']]
    layout = [
        # [sg.T('Channel Config', font='DEFAIULT 18')],
        [sg.Table(values=val, headings=headers,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='center', key='-TABLE-',
                  selected_row_colors='red on yellow',
                  enable_events=False,
                  expand_x=True,
                  expand_y=True,
                  enable_click_events=True, right_click_selects=True, right_click_menu=right_click_menu_def)],
        [sg.B('Ok'), sg.B('Cancel')],
    ]

    window = sg.Window('Channel Config', layout, keep_on_top=True)
    selected_cell = None
    while True:
        event: str
        event, values = window.read(timeout=100)

        # todo this is for development
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print(f'============ Event = {event} ==============')

        # dont save if canceled
        if event in (None, 'Cancel', sg.WIN_CLOSED):
            return False, {}

        # table editing
        elif '-TABLE-' in event:
            selected_cell = event[2]
            print(f'You selected row {selected_cell}')
        elif 'Delete' in event:
            del conf.channels[selected_cell[0]]
            print(f'deleted cell {selected_cell[0]}')

        # elif 'Add' in event:  # todo flesh out add and clone
        #     channel = channels.ChannelElement('test', 412, 412487500, 'BULK UP')
        #     config['channels'].append(channel.values())
        elif 'Clone' in event:
            if selected_cell is not None:
                changed, new_conf = edit_channel_window(conf, selected_cell[0])
                if changed:
                    conf = new_conf
                    del conf
                print(f'Cloned Channel {selected_cell[0]}')
        elif 'Edit' in event:
            if selected_cell is None:
                print('no cell selected')
                continue
            else:
                print(f'cell selected {selected_cell[0]}')

                changed, conf = edit_channel_window(conf, selected_cell[0])
            if changed:
                print('config changed')
                config = conf
                del conf

        elif event.lower() in ('add'):
            changed, new_conf = edit_channel_window(conf, None)
            if changed:
                print('config changed')
                config = new_conf
                del conf

            # print(f'Edited Channel {selected_cell[0]}')

        # save settings
        elif event == 'Ok':
            # sg.user_settings_set_entry('-theme-', values['-THEME-'])
            return True, conf
        # updated_list = [val for index in config['channels'] val in config['channels'][i].__dict__.values()]
        # print(updated_list)
        # window['-TABLE-'].update(values=)


# def dict_to_list(d: dict, key: str) -> list:
#     if key not in d.keys():
#         return []
#     else:
#         return [k[key] for k in d[key]]


def edit_channel_window(config: dict, key: int) -> (bool, dict):
    """

    Show the channel edit window

    """

    working_config = config

    if isinstance(key, int):
        current = working_config['channels'][key]
    else:
        current = ('', 0, 'PRIORITY', 0)

    print(current)
    # users parameters from class
    edit_channel_window_layouts = {
        'name': [sg.T('Name'), sg.Push(), sg.Input(default_text=current[0], key='-NAME-', size=10, )],
        'center': [sg.T('Center'), sg.Push(),
                   sg.Combo(default_value=current[1], values=[],  #[f for f in working_config.channels if f.e] , #channels.enabled_frequencies(working_config),
                            readonly=False, k='-CENTER-', size=11)],
        'channel_type': [sg.T('Channel Type'), sg.Push(),
                         sg.Combo(default_value=current[2], values=list(working_config.channel_types),
                                  readonly=False, k='-CH_TYPE-', size=11)],
        'fpga': [sg.T('FPGA'), sg.Push(), sg.T(key='-FPGA-', size=10, )],
    }

    layout = [[], ]

    for key in config.annel_headers:
        layout += [edit_channel_window_layouts[key.lower()]]

    layout += [[sg.B('Ok'), sg.B('Cancel')]]
    window = sg.Window('Channel ', layout, keep_on_top=True)

    # editing loop
    while True:
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print(f'============ Event = {event} ==============')

        if event in (None, 'Exit', 'Cancel'):
            window.close()
            break

        if 'Ok' in event:
            fields = values['-NAME-'], values['-CENTER-'], values['-CH_TYPE-']
            # empty_count = [f for f in fields if f == '']
            if fields.count('') > 0:
                sg.popup_ok('Fields can not be empty', background_color='red', keep_on_top=True)
                continue
            elif current[0] == values['-NAME-']:
                sg.popup_ok('Unique Names Only', background_color='red', keep_on_top=True)
                continue
            working_config['channels'].append(fields)
            # print(values['-NAME-'], values['-BASE-'], values['-CENTER-'], values['-CH_TYPE-'])
            window.close()
            return True, working_config

    return False, {}
