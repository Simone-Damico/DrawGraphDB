import shutil
import errno


def copy(src, dest):
    """
    Function used for copy a hierarchy of directory from src to dest
    :param src: The directory to copy from
    :param dest: The directory in which to copy
    :except errno.ENOTDIR: if the source isn't a directory
    """
    try:
        shutil.copy(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


def choise_to_string(lis):
    """
    Function used for convert a list of element in a string that represent a list of tuple used for a choice field in
    the models.

    :param lis: A list of element to convert
    :return res: A tuple of tuple like a string
    """
    res = '('
    for elem in lis:
        res = res + "('" + elem + "', '" + elem + "'), "
    res = res[:len(res)-2]
    res = res + ')'
    return res


# Funzione che presa una lista di liste restituisce una lista di tuple
def unique_to_tuple(lis):
    """
    Function used for convert a list of list in a list of tuple.

    :param lis: A list of list to convert
    :return res: A list of tuple
    """
    res = []
    for elem in lis:
        res.append(tuple(elem))
    return res


def indent(level):
    """
    Function used for the indentation of python code. It returns multiple of 4 spaces.

    Parameters:
    level (int): The level indicates the level of indentation, the spaces returned are 4 multiplied by level.

    Returns:
    string: spaces for the indentation of python code.
    """
    return ' ' * (4 * level)