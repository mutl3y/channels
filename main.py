import gui, utils
from dataclasses import dataclass, field, asdict, astuple
import user_interfaces
import _channels
from persistence.data_class_storage import SaveAsYaml
import _channels


def main(app_settings: _channels.ConfigData):
    # Start a gui with the configuration as set
    ui = user_interfaces.new_ui('gui')
    print(app_settings)
    changed, config = ui.edit(a_dict=asdict(app_settings), title='channels', lookup=app_settings.lookups())
    if changed: # editor says file was changed
        print('config changed')
        app_settings.update(config)
        app_settings.save(app_settings.filename)
        del config


if __name__ == '__main__':
    cfg = _channels.config_factory()
    main(cfg)
