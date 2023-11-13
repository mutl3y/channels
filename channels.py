import PySimpleGUI as sg
import settings as Settings

from enum import Enum

max_channels = 48
channelList = []



class ChannelElement:
    def __init__(self, name: str, carrier: int, base: int, center: int, ch_type: str):
        super().__init__()
        self.name = name
        self.carrier = carrier
        self.base = base
        self.center = center
        self.ch_type = ch_type

    def __str__(self):
        return f'{self.name}, {self.carrier}, {self.base}, {self.center}, {self.ch_type} '

    def keys(self):
        return list(self.__dict__)

    def values(self):
        return [self.name, self.carrier, self.base, self.center, self.ch_type]

    # def save(self, filename=):


h = ChannelElement('test', 1, 1, 1, 'bulk')

headers = [header.capitalize() for header in h.keys()]

# del ch
# print(headers)
# exit(0)
rows = []

rows.append(h.values())
rows.append(h.values())
rows.append(h.values())


def Channels_window(theme='bluePurple', filename='channel_settings'):
    """
    Show the channel configuration window

    # :return: True if settings were changed
    # :rtype: (bool)
    """
    sg.user_settings_filename(filename=filename)

    right_click_menu_def = [[], ['Add', 'Edit ', 'Clone', 'Delete']]
    layout = [
        # [sg.T('Channel Config', font='DEFAIULT 18')],
        [sg.Table(values=rows, headings=headers,
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

    ch_popup_layout = [[sg.Text("Popup Testing")],
                       [sg.Button("Open Folder")],
                       [sg.Button("Open File")]]

    window = sg.Window('Channel Config', layout, keep_on_top=True)
    selected_cell = None
    while True:
        event, values = window.read(timeout=100)

        # todo this is for development
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print(f'============ Event = {event} ==============')

        # dont save if canceled
        if event in (None, 'Cancel', sg.WIN_CLOSED):
            return False

        # save settings
        elif event == 'Ok':
            sg.user_settings_set_entry('-theme-', values['-THEME-'])
            return True

        # table editing
        elif '-TABLE-' in event:
            selected_cell = event[2]
            print(f'You selected row {selected_cell}')
        elif 'Delete' in event:
            del rows[selected_cell[0]]
            print(f'deleted cell {selected_cell[0]}')
            print(rows)
        elif 'Add' in event:
            channel = ChannelElement('test', 1, 1, 1, 'bulk')
            rows.append(channel.values())
        elif 'Clone' in event:
            channel = ChannelElement('test', 1, 1, 1, 'bulk')
            # rows.append(rows[selected_cell[0]])

            EditChannelWindow(selected_cell[0])
            print(f'Cloned Channel {selected_cell[0]}')
        window['-TABLE-'].update(values=rows)

    # [sg.T('Channel', font='DEFAIULT 18')],
    # [sg.Table(values=rows, headings=headers,
    #

    #           display_row_numbers=False,
    #           justification='center', key='-TABLE-',
    #           selected_row_colors='red on yellow',
    #           enable_events=False,
    #           expand_x=True,
    #           expand_y=True,
    #           enable_click_events=True)],  # , right_click_selects=True, right_click_menu=right_click_menu_def)],


def EditChannelWindow(config, key):
    """

    Show the channel edit window

    """
    # selected_row = table[row]
    print(settings.config['channels'])

    edit_channel_window_layouts = {
        'name':    [sg.T('Name'), sg.Push(), sg.Input(key='-NAME-', size=10, )],
        'carrier': [sg.T('Carrier'), sg.Push(),
                    sg.Combo(values=(settings.enabled_frequencies()), size=11, k='-CARRIER-', readonly=False)],
        'base':    [sg.T('Base'), sg.Push(), sg.Combo(values=(), k='-BASE-', readonly=False, size=11)],
        'center':  [sg.T('Center'), sg.Push(), sg.Combo(values=(), readonly=False, k='-CENTER-', size=11)],
        'ch_type': [sg.T('Channel Type'), sg.Push(), sg.Combo(default_value=(config['ch_types'][0]), values=(config['ch_types']), readonly=False, k='-CH_TYPE-', size=11)],
        }

    layout = [[], ]

    k = 0
    for key in headers:
        # print(key, ': ', selected_row[k])
        layout += [edit_channel_window_layouts[key.lower()]]
        k += 1

    layout += [[sg.B('Ok'), sg.B('Cancel')]]
    window = sg.Window('Channel ', layout, keep_on_top=True)

    # editing loop
    while True:
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print(f'============ Event = {event} ==============')
            # print('-------- Values Dictionary (key=value) --------')  # for key in values:  #     print(key, ' = ', values[key])
        if event in (None, 'Exit', 'Cancel'):
            break
        if 'Ok' in event:
            fields = values['-NAME-'], values['-CARRIER-'], values['-BASE-'], values['-CENTER-'], values['-CH_TYPE-']
            empty_count = [f for f in fields if f == '']
            if fields.count('') > 0:
                sg.popup_ok('Fields can not be empty', background_color='red', keep_on_top=True)
                continue

            config['frequencies'][values['-NAME-']] = int(values['-CARRIER-'])
            # table[row] = [fields]

            window.close()
            break


if __name__ == '__main__':
    settings = Settings.Settings()
    # print(settings.config)
    # EditChannelWindow(settings.config, key='413256500')
    # print(rows)
    Channels_window()
