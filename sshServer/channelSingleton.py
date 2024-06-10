class ChannelSingleton(object):
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance=super(ChannelSingleton,cls).__new__(cls)
        return cls.instance