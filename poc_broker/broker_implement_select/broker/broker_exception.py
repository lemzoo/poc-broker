#! /usr/bin/python
class ExchangeNotDefinedYet(Exception):
    pass


class ExchangeAlreadyInUse(Exception):
    pass


class ChannelDoesntExist(Exception):
    pass


class ChannelIsAlreadyInUse(Exception):
    pass


class ConnectionIsOffline(Exception):
    pass


class ConnectionIsAlreadyInUse(Exception):
    pass
