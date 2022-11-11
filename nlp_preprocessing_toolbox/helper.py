from difflib import ndiff

def levenshtein_distance(str1, str2, ):
    counter = {"+": 0, "-": 0}
    distance = 0
    for edit_code, *_ in ndiff(str1, str2):
        if edit_code == " ":
            distance += max(counter.values())
            counter = {"+": 0, "-": 0}
        else: 
            counter[edit_code] += 1
    distance += max(counter.values())
    return distance

def to_lower(word: str):
    tolower_text = (word.replace('İ', 'i'))
    tolower_text = (tolower_text.replace('I', 'ı'))
    return tolower_text.lower()


def _decode(string: str) -> str:
    """
    Bu fonksiyon unidecode kütüphanesinden alınmış ve türkçe için özelleştirilmiştir.
    Türkçe için genişletilmiş Ascii çevirici.
    :param string: unicode string
    :return: Tr Ascii string
    """
    cache = {}
    decval = []

    for char in string:
        codepoint = ord(char)

        if codepoint in {199, 214, 220, 231, 246, 252, 286, 287, 304, 305, 350, 351, 8364, 8378, 8240}:
            decval.append(str(char))
            continue

        if codepoint < 0x80:
            decval.append(str(char))
            continue

        if codepoint > 0xeffff:
            continue

        section = codepoint >> 8
        position = codepoint % 256

        if section in cache:
            table = cache[section]
        else:
            try:
                mod = __import__('unidecoder.x%03x' % section, fromlist=['data'])
            except ImportError:
                cache[section] = None
                continue
            cache[section] = table = mod.data

        if table and len(table) > position:
            decval.append(table[position])

    return ''.join(decval)

def unitoascii(string: str) -> str:
    """
    Türkçe için genişletilmiş Ascii çevirici.
    :param string: unicode string
    :return: Tr Ascii string
    """
    try:
        string.encode('ASCII')
    except UnicodeEncodeError:
        return _decode(string)

    return string