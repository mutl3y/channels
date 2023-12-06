
def fpga_to_hz(var):
    return (6250 * int(var)) + 409600000


def hz_to_fpga(var):
    return int((var - 409600000) / 6250)
