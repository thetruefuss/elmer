def check_image_extension(filename):
    ext = ['.jpg', '.jpeg', '.png']
    for e in ext:
        if filename.endswith(e):
            return True
    return False
