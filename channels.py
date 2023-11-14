import settings.config as settings
import gui, utils
from _channels import Channel

channelList = []


def default_config() -> dict:
    freq_list = [{'fpga': fpga, 'hz': utils.fpga_to_hz(fpga), 'enabled': True} for fpga in
                 range(200, 202)]

    return dict(frequencies=freq_list, channel_types=['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS'], channels=[],
                channel_groups=[], towers=[], max_channels=48
                )


def enabled_frequencies(d: dict) -> list:
    if 'frequencies' not in d.keys():
        return []
    else:
        return [i['hz'] for i in d['frequencies'] if i['enabled']]


if __name__ == '__main__':
    app_settings = settings.Settings()
    # app_settings.read_config()
    if isinstance(app_settings, object):
        print('Creating default config')

    app_settings.write_default_config(default_config())

    # todo test code
    h = Channel('test', 1, 'BULK UP')
    headers = [header.capitalize() for header in h.keys()]



    app_settings.config['channels'].append(h.values())
    app_settings.config['channels'].append(h.values())
    app_settings.write_config()
    print(list(app_settings.config['channels']))

    app_settings.config['channel_headers'] = headers
    app_settings.config['theme'] = 'bluePurple'
    app_settings.write_config()
    changed, config = gui.channels_window(app_settings.config)
    if changed:
        app_settings.write_default_config(config)
        del config
