class EzawsBaseException(Exception):
    """General base exception except for exceptions that inherit from boto3."""

    pass


class CloudWatchException(EzawsBaseException):
    pass


class RDSException(EzawsBaseException):
    pass
