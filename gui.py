#!/usr/bin/env python3

import PySimpleGUI
import time


def decode(d: dict) -> (str, list, list):
    print(f'data in : {d}')

    title = str(list(d.keys())[0])
    print(f'title: {title}')

    _data = d[title]
    print(f'debug _list is_list:{isinstance(_data, list)} \n')

    if isinstance(_data[0], list):
        print('***** list ******')
    if isinstance(_data[0], dict):
        headers = list(_data[0].keys())
        list_out = [list(li.values()) for li in _data]

        # todo cleanup
        print(f'***** dict : {headers}')
        print(f'list out: \n{list_out[0]}\n')
    elif isinstance(_data[0][0], list):
        print(f'***** list : {_data[0][0]}')
        headers = title
        list_out = [li for li in _data]

    else:
        headers = 'oops'
        list_out = [li for li in _data]

    return title, headers, list_out


def pack(header, list_in) -> dict:
    return {header: list_in}


# def dead():
#     """ delete me #todo """
#     # headers = list(a_dict.keys())
#     d = dict()
#     for i in a_dict.fromkeys():
#         print(i)
#         # data = a_dict.values()
#         # print(f'Header = {header}')
#         print(f'Data   = {i}')
#         # if isinstance(data, list):
#         #     # d[header] = dict(data)
#         #     print(dict(d))
#         #     print('list')
#
#     # data = [{item: item} for item in headers if not isinstance(item, list)]
#
#     return headers, d


def edit_channels(a_dict: dict, auto_close: int = None) -> (bool, dict):
    # right_click_menu_def: list = ['Add', 'Edit ', 'Clone', 'Delete'])
    """
    Show the channel configuration window

    # :return: True if settings were changed
    # :rtype: (bool)
    """
    # headers = list(a_dict.keys())
    # data = [list(a_dict[item]) for item in a_dict if not isinstance(item, list)]
    # print(a_dict)
    title, headers, data = decode(a_dict)
    # print(f'decoded data structure\n{data}')
    #
    # print(f'Incoming data {a_dict[title]}')  # todo remove
    # print(f'Headers: {headers}\nData: {data}')  # todo

    # right_click_menu = [[]].append(right_click_menu_def)
    right_click_menu_def = [[], ['Add', 'Edit ', 'Clone', 'Delete']]
    layout = [
        [PySimpleGUI.Table(values=data, headings=headers, auto_size_columns=True, display_row_numbers=False,
                           justification='center', key='-TABLE-', selected_row_colors='red on yellow',
                           enable_events=False, expand_x=True, expand_y=True, enable_click_events=True,
                           right_click_selects=True, right_click_menu=right_click_menu_def)],
        [PySimpleGUI.B('Ok'), PySimpleGUI.B('Cancel')],
    ]

    window = PySimpleGUI.Window(title=title, layout=layout, keep_on_top=True, auto_close=isinstance(auto_close, int),
                                auto_close_duration=auto_close)
    selected_row = tuple()
    window.refresh()
    # print(layout)
    test_events = ['Edit']
    # selected_row = 0
    # values = [1, 2, 3]
    # #     '-TABLE-  +CLICKED+ ', (1, 1)),
    # #     ('Edit',1)
    # # ]
    # x = 0
    while True:
        # x += 1
        # if x <= 3:
        #     break
        # time.sleep(1)
        # event: str = 'Edit'
        # values = data[0]
        event, values = window.read(timeout=100)

        # event, [1,2,3] = test_events.pop(0)
        # todo this is for development
        if event not in (PySimpleGUI.TIMEOUT_EVENT, PySimpleGUI.WIN_CLOSED, 'Delete'):
            print(f'============ Event = {event} ==============')
            print(event)
            print(values)
        if event in (None, 'Cancel', PySimpleGUI.WIN_CLOSED):
            pass
            # return False, None
        elif '-TABLE-' and '+CLICKED+' in event:
            if len(values['-TABLE-']) > 0:
                selected_row = values['-TABLE-'][0]
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
            if selected_row is None:
                print('no cell selected')
                continue
            else:
                # print(f'try editing {data[selected_row]}')
                changed, di = edit_channels(pack(title, data[selected_row]))
                if changed:
                    data[selected_row] = di.values()
                return changed, data
                # print()
                # changed, conf = edit_channels(conf, selected_cell[0])
            # if changed:
            #     print('config changed')
            #     config = conf
            #     del conf

        elif 'Add' in event:
            # changed, new_conf = edit_channel_window(conf, None)
            # if changed:
            #     print('config changed')
            #     config = new_conf
            #     del conf
            pass
            # print(f'Edited Channel {selected_cell[0]}')

            # save settings
        elif event == 'Ok':
            # sg.user_settings_set_entry('-theme-', values['-THEME-'])
            return True, data
            # updated_list = [val for index in config['channels'] val in config['channels'].[i].__dict__.values()]
            # print(updated_list)
        # print(list_data)
        window['-TABLE-'].update(values=data)

# # def edit_channel(d: dict) -> (bool, dict):
# #     edit_channel_window_layouts = {
# #         'name': [sg.T('Name'), sg.Push(), sg.Input(default_text=current[0], key='-NAME-', size=10, )],
# #         'center': [sg.T('Center'), sg.Push(),
# #                    sg.Combo(default_value=d, values=[],
# #                             # [f for f in working_config.channels if f.e] , #channels.enabled_frequencies(working_config),
# #                             readonly=False, k='-CENTER-', size=11)],
# #         'channel_type': [sg.T('Channel Type'), sg.Push(),
# #                          sg.Combo(default_value=current[2], values=list(working_config.channel_types),
# #                                   readonly=False, k='-CH_TYPE-', size=11)],
# #         'fpga': [sg.T('FPGA'), sg.Push(), sg.T(key='-FPGA-', size=10, )],
# #     }
# #
# #     layout = [[], ]
# #     headers = [header.capitalize() for header in d.keys()]
# #
# #     for key in headers:
# #         layout += [edit_channel_window_layouts[key.lower()]]
# #
# #     layout += [[sg.B('Ok'), sg.B('Cancel')]]
# #     window = sg.Window('Channel ', layout, keep_on_top=True, auto_close_duration=5, auto_close=True)
# #
# #     return True, d
# #
#
# def channels_window(conf: dict, theme: str = 'bluePurple', test=False) -> (bool, dict):
#     """
#     Show the channel configuration window
#
#     # :return: True if settings were changed
#     # :rtype: (bool)
#     """
#     try:
#         sg.Theme = conf.theme
#     except:
#         sg.Theme = theme
#     selected_cell = None
#
#     val = [list(i.values()) for i in conf['channels']]
#     headers = [header.capitalize() for header in conf['channels'][0].keys()]
#     print(headers)
#     right_click_menu_def = [[], ['Add', 'Edit ', 'Clone', 'Delete']]
#     layout = [
#         # [sg.T('Channel Config', font='DEFAIULT 18')],
#         [sg.Table(values=val, headings=headers,
#                   auto_size_columns=True,
#                   display_row_numbers=False,
#                   justification='center', key='-TABLE-',
#                   selected_row_colors='red on yellow',
#                   enable_events=False,
#                   expand_x=True,
#                   expand_y=True,
#                   enable_click_events=True, right_click_selects=True, right_click_menu=right_click_menu_def)],
#         [sg.B('Ok'), sg.B('Cancel')],
#     ]
#     if test:
#         return True, conf
#
#     window = sg.Window('Channel Config', layout, keep_on_top=True)
#     selected_cell = None
#     while True:
#         event: str
#         event, values = window.read(timeout=100)
#
#         # todo this is for development
#         if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
#             print(f'============ Event = {event} ==============')
#
#         # dont save if canceled
#         if event in (None, 'Cancel', sg.WIN_CLOSED):
#             return False, {}
#
#         # table editing
#         elif '-TABLE-' in event:
#             selected_cell = event[2]
#             print(f'You selected row {selected_cell}')
#         elif 'Delete' in event:
#             del conf['channels'][selected_cell[0]]
#             print(f'deleted cell {selected_cell[0]}')
#
#         # elif 'Add' in event:  # todo flesh out add and clone
#         #     channel = channels.ChannelElement('test', 412, 412487500, 'BULK UP')
#         #     config['channels'].append(channel.values())
#         elif 'Clone' in event:
#             if selected_cell is not None:
#                 changed, new_conf = edit_channel_window(conf, selected_cell[0])
#                 if changed:
#                     conf = new_conf
#                     del new_conf
#                 print(f'Cloned Channel {selected_cell[0]}')
#         elif 'Edit' in event:
#             if selected_cell is None:
#                 print('no cell selected')
#                 continue
#             else:
#                 print(f'cell selected {selected_cell[0]}')
#
#                 changed, conf = edit_channel_window(conf, selected_cell[0])
#             if changed:
#                 print('config changed')
#                 config = conf
#                 del conf
#
#         elif event.lower() in ('add'):
#             changed, new_conf = edit_channel_window(conf, None)
#             if changed:
#                 print('config changed')
#                 config = new_conf
#                 del conf
#
#             # print(f'Edited Channel {selected_cell[0]}')
#
#         # save settings
#         elif event == 'Ok':
#             # sg.user_settings_set_entry('-theme-', values['-THEME-'])
#             return True, conf
#         # updated_list = [val for index in config['channels'] val in config['channels'].[i].__dict__.values()]
#         # print(updated_list)
#         window['-TABLE-'].update(values=conf['channels'])
#
#
# # def dict_to_list(d: dict, key: str) -> list:
# #     if key not in d.keys():
# #         return []
# #     else:
# #         return [k[key] for k in d[key]]
#
#
# def edit_channel_window(d: dict, key: int) -> (bool, dict):
#     """
#
#     Show the channel edit window
#
#     """
#
#     working_config = d
#
#     if isinstance(key, int):
#         current = working_config['channels'][key]
#     else:
#         current = ('', 0, 'PRIORITY', 0)
#
#     print(current)
#     edit_channel_window_layouts = {
#         'name': [sg.T('Name'), sg.Push(), sg.Input(default_text=current[0], key='-NAME-', size=10, )],
#         'center': [sg.T('Center'), sg.Push(),
#                    sg.Combo(default_value=current[1], values=[],
#                             # [f for f in working_config.channels if f.e] , #channels.enabled_frequencies(working_config),
#                             readonly=False, k='-CENTER-', size=11)],
#         'channel_type': [sg.T('Channel Type'), sg.Push(),
#                          sg.Combo(default_value=current[2], values=list(working_config.channel_types),
#                                   readonly=False, k='-CH_TYPE-', size=11)],
#         'fpga': [sg.T('FPGA'), sg.Push(), sg.T(key='-FPGA-', size=10, )],
#     }
#
#     layout = [[], ]
#     headers = [header.capitalize() for header in d['channels'][0].keys()]
#
#     for key in headers:
#         layout += [edit_channel_window_layouts[key.lower()]]
#
#     layout += [[sg.B('Ok'), sg.B('Cancel')]]
#     window = sg.Window('Channel ', layout, keep_on_top=True)
#
#     # editing loop
#     while True:
#         event, values = window.read(timeout=100)
#         # keep an animation running so show things are happening
#         if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
#             print(f'============ Event = {event} ==============')
#
#         if event in (None, 'Exit', 'Cancel'):
#             window.close()
#             break
#
#         if 'Ok' in event:
#             fields = values['-NAME-'], values['-CENTER-'], values['-CH_TYPE-']
#             # empty_count = [f for f in fields if f == '']
#             if fields.count('') > 0:
#                 sg.popup_ok('Fields can not be empty', background_color='red', keep_on_top=True)
#                 continue
#             elif current[0] == values['-NAME-']:
#                 sg.popup_ok('Unique Names Only', background_color='red', keep_on_top=True)
#                 continue
#             working_config['channels'].append(fields)
#             # print(values['-NAME-'], values['-BASE-'], values['-CENTER-'], values['-CH_TYPE-'])
#             window.close()
#             return True, working_config
#
#     return False, {}
