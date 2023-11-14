class Channel(object):
    def __init__(self, name: str, center: int, channel_type: str):
        self.name = name
        self.center = center
        self.channel_type = channel_type

    def __str__(self) -> str:
        return f'{self.name}, {self.center}, {self.channel_type}'

    def keys(self) -> list:
        return list(self.__dict__)

    def values(self) -> list:
        return [self.name, self.center, self.channel_type]

    def fpga(self):
        return (6250 * self.center) + 409600000

