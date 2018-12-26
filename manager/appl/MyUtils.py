import shutil
import errno
import json


# Copia la gerarchia di cartelle e file da src a dest


def copy(src, dest):
    try:
        shutil.copy(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


# Funzioni per il coricamento del JSON che ritornano stringhe e non UNICODE
def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


# Funzione che presa una lista di elementi per un campo choice crea una tupla di tuple e la restituisce come stringa
def choise_to_string(lista):
    res = '('
    for elem in lista:
        res = res + "('" + elem + "', '" + elem + "'), "
    res = res[:len(res)-2]
    res = res + ')'
    return res


# Funzione che presa una lista di liste restituisce una lista di tuple
def unique_to_tuple(lista):
    res = []
    for l in lista:
        res.append(tuple(l))
    return res
