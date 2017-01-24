#! /usr/bin/python
class ExchangeNotDefinedYet(Exception):
    pass


class ExchangeAlreadyExist(Exception):
    pass


class ChannelDoesntExist(Exception):
    pass


class ChannelIsAlreadyInUse(Exception):
    pass


class ConnectionNotOpenedYet(Exception):
    pass


class ConnectionIsAlreadyInUse(Exception):
    pass


class QueueNameDoesntMatch(Exception):
    pass


class ExchangeNameDoesntMatch(Exception):
    pass


class BasicPropertiesIsNotSet(Exception):
    pass
