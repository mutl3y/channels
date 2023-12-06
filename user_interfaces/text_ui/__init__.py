import curses, time
from curses import wrapper
from curses.textpad import Textbox, rectangle


def main(stdstr, c):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    y = 0
    x = 0
    stdstr.clear()
    max_y, max_x = stdstr.getmaxyx()

    pad = curses.newpad(200, 200)
    stdstr.refresh()
    pad.addstr(str(stdstr.getmaxyx()))

    for key, value in c.items():
        if isinstance(value, list):
            pad.addstr(y, 0, f'{key}: ')
            if len(value) == 0:
                pad.addstr(y, 0, key + ': ' + str(value))
                x = 0
            elif isinstance(value[0], str):
                pad.addstr(y, 0, key + ': ' + str(value))
                x = 0
            elif isinstance(value[0], dict):
                x += 4
                for v in value:
                    y += 1
                    pad.addstr(y, x, str(v))
                x = 0
            else:
                pad.addstr(str(type(value[0])))
        else:
            x = 0
            pad.addstr(y, x, key + ': ' + str(value))
        y += 1
    pad.nodelay(True)
    px, py = 0, 0
    pad.clear()
    while True:
        key: str = ''
        try:
            key = pad.getkey()
            pad.addstr(key)
            if key in ['q', 'Q']:
                break
            elif key in [curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT]:
                pad.addstr(f'arrow key detected {key}')
                if key == curses.KEY_UP:
                    py -= 1
                    if py < 1:
                        py = 0
                elif key == curses.KEY_DOWN:
                    py -= 1
                    if py >= max_y - 1:
                        py = max_y - 1
                elif key == curses.KEY_LEFT:
                    px -= 1
                    if px <= 0:
                        px = 0
                elif key == curses.KEY_RIGHT:
                    px += 1
                    if px >= max_x - 1:
                        px = max_x - 1
            else:
                pad.addstr(key)

        except Exception as e:
            print(e)
            pass

        pad.refresh(0, 0, 5, 5, 10, 10)
        time.sleep(0.5)


if __name__ == '__main__':
    config = {
        'channel_groups': [],
        'channel_headers': ['Name', 'Center', 'Channel_type'],
        'channel_types': ['BULK UP', 'BULK DOWN', 'L2ACK', 'PRIORITY', 'RTS'],
        'channels': [
            {'name': 'test', 'center': 1, 'channel_type': 'BULK'}
        ],
        'frequencies': [
            {'enabled': True, 'fpga': 200, 'hz': 410850000},
            {'enabled': True, 'fpga': 201, 'hz': 410856250}
        ],
        'max_channels': 48,
        # 'theme': 'bluePurple',
        'towers': []
    }
    wrapper(main, config)
    # main()
