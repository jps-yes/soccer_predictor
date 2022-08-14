global debug_mode


def init():
    response_debug_mode = input('Do you want to run in debug mode? (Y/N): ')
    if response_debug_mode == 'Y':
        debug_mode = True
    else:
        debug_mode = False

