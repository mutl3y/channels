import gui, utils
from dataclasses import dataclass, field, asdict, astuple
import _channels
from persistence.data_class_storage import SaveAsYaml
import _channels

def main(app_settings: _channels.ConfigData):
    print(f' {type(app_settings)}')
    changed, config = gui.channels_window(asdict(app_settings), test=True)
    if changed:
        print('config changed')
        app_settings.update(config)
        app_settings.save(app_settings._filename)
        del config


if __name__ == '__main__':
    cfg = _channels.config_factory()
    print(cfg)
    main(cfg)
