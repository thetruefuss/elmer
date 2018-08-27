def check_image_extension(filename):
    """
    Checks filename extension.

    :param filename: string
    :return: boolean
    """
    ext = ['.jpg', '.jpeg', '.png']
    for e in ext:
        if filename.endswith(e):
            return True
    return False
