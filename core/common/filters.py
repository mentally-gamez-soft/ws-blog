"""Define all the filters for the application."""


def format_datetime(value, format="short"):
    """Define a formatter for the datetime.

    Args:
        value (date): the datetime.
        format (str, optional): the format to apply 'full' or 'short'. Defaults to "short".

    Returns:
        _type_: _description_
    """
    value_str = None
    if not value:
        value_str = ""
    if format == "short":
        value_str = value.strftime("%d/%m/%Y")
    elif format == "full":
        value_str = value.strftime("%d de %m de %Y")
    else:
        value_str = ""
    return value_str
