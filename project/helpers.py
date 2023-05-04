import re
from copy import copy
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def string_to_tuple(string):
    try:
        string = string[1:-1]
        elements = string.split(',')
        result = ()
        for e in elements:
            if e:
                if e[0] == '0': e = e[1:]
                result += (int(e), )
    except:
        return None
    return result


# simple Uzbek cyrillic to latin translator
apostrophes = ['‘', '˘', '’', '`']
format_characters = ['*', '~', '`', '__']

cyrillic_lower = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',
    'д': 'd', 'ё': 'yo', 'ж': 'j', 'ц': '',
    'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
    'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
    'п': 'p', 'р': 'r', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'x', 'ч': 'ch', 'е': '',
    'ш': 'sh', 'ъ': "'", 'ь': '', 'э': 'e',
    'ю': 'yu', 'я': 'ya', 'ў': "o'", 'қ': 'q',
    'ғ': "g'", 'ҳ': 'h', 'с': 's'
}

cyrillic_upper = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G',
    'Д': 'D', 'Ё': 'Yo', 'Ж': 'J',
    'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K',
    'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
    'П': 'P', 'Р': 'R', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'X', 'Ч': 'Ch',
    'Ш': 'Sh', 'Ъ': "'", 'Ь': '', 'Э': 'E',
    'Ю': 'Yu', 'Я': 'Ya', 'Ў': "O'", 'Қ': 'Q',
    'Ғ': "G'", 'Ҳ': 'H', 'С': 'S'}

cyrillic_upper_spec = ['Ё', 'Ю', 'Я', 'Ш', 'Ч', 'Ц', 'Е']


def cyrillic_to_latin(text):
    for i, c in enumerate(text):
        if c in format_characters:
            result[i] = ' '
        elif c in apostrophes:
            result[i] = "'"
        elif c in ['ц', 'Ц']:
            if is_vowel(result[i - 1]):
                result[i] = "ts"
            else:
                result[i] = "s"
        elif c in ['е', 'Е']:
            if is_consonant(result[i - 1]):
                result[i] = 'e'
            else:
                result[i] = 'ye'
        elif c in cyrillic_lower:
            result[i] = cyrillic_lower[c]
        elif c in cyrillic_upper:
            result[i] = cyrillic_upper[c]
        else:
            result[i] = c
        if c in cyrillic_upper_spec:
            if (i == 0 or text[i - 1].isspace()) and (i == len(text) - 1 or text[i + 1] in cyrillic_lower or ord(text[i + 1]) in range(97, 123)):
                result[i] = result[i].title()
            else:
                result[i] = result[i].upper()
    return "".join(result)


def is_vowel(c):
    try:
        return c[-1].lower() in ['a', 'e', 'i', 'u', 'o'] or c == "o'"
    except IndexError:
        return False

def is_consonant(c):
    try:
        return c[-1].lower() in [
            'b', 'd', 'f', 'g', 'h', 'j',
            'k', 'l', 'm', 'n', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'x', 'y'
        ] or c == "g'"
    except IndexError:
        return False


# determines and drops channel`s common ending from each message
# it also checks if message is advertisement
def drop_channel_sign(messages):
    messages = [re.split(' |\n', m.strip()) for m in messages]
    possible_suffix = check_for_common_suffix(messages)

    common_suffix = ''

    if possible_suffix:
        common_suffix, ad = determine_common_suffix(messages, possible_suffix)
        for i in range(len(messages)):
            if not ad[i]:
                messages[i] = messages[i][:-len(common_suffix)]
    else:
        ad = [0 for t in messages]

    # drop hashtages from messages and return result
    return [" ".join([w for w in m if len(w) > 0 and w[0] != '#']) for m in messages], ad


def check_for_common_suffix(messages):
    for m in messages:
        similars = 0
        for n in messages:
            if n[-1] == m[-1]:
                similars += 1
                if similars >= len(messages) / 2:
                    return m
    return []


def determine_common_suffix(messages, possible_suffix):
    ad, common_suffix = [], possible_suffix
    for m in messages:
        if m[-1] == common_suffix[-1]:
            ad.append(0)
            common_suffix = common_suffix[-len(m):]
            temp = copy(m[-len(common_suffix):])
            for i in range(len(temp) - 1, -1, -1):
                if temp[i] != common_suffix[i]:
                    common_suffix = common_suffix[i+1:]
                    break
        else:
            ad.append(1)
    return common_suffix, ad