from dataclasses import asdict
import user_interfaces
from AppConfig import settings


def main(app_settings: settings.ConfigData):
    # Start a gui with the configuration as set
    ui = user_interfaces.new_ui('gui')
    print(app_settings)
    changed, config = ui.edit(a_dict=asdict(app_settings), title='FE', lookup=app_settings.lookups())
    if changed:  # editor says file was changed
        print('config changed')
        app_settings.update(config)
        app_settings.save(app_settings.filename)
        del config


if __name__ == '__main__':
    cfg = settings.config_factory()
    main(cfg)
