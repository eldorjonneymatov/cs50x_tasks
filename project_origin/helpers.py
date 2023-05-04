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

latin_lower = [str(i) for i in range(97, 123)]
cyrillic_upper_spec = ['Ё', 'Ю', 'Я', 'Ш', 'Ч', 'Ц', 'Е']


def cyrillic_to_latin(text):
    result = ['' for i in text]
    for i, c in enumerate(text):
        if c in apostrophes:
            result[i] = "'"
        elif c in ['ц', 'Ц']:
            result[i] = "ts" if is_vowel(result[i - 1]) else "s"
        elif c in ['е', 'Е']:
            result[i] = "e" if is_consonant(result[i - 1]) else "ye"
        elif c in cyrillic_lower:
            result[i] = cyrillic_lower[c]
        elif c in cyrillic_upper:
            result[i] = cyrillic_upper[c].lower()
        elif c.isalpha():
            result[i] = c.lower()
        elif c.isspace() or c.isdigit():
            result[i] = c
        # these characters are then used to define hashtags and usernames
        elif c in ['#', '@']:
            result[i] = c
        # this trick then used to drop links
        elif c == ']' and i < len(text) - 1 and text[i + 1] == '(':
            result[i] = ' @'
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
def drop_channel_sign(messages_list):
    messages = []
    for m in messages_list:
        temp = re.split(' |\n|\t', m.strip())
        temp = [w for w in temp if w and not w[0] in ['#', '@']]
        messages.append(temp)
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
    return [" ".join(m) for m in messages], ad


def check_for_common_suffix(messages):
    for m in messages:
        if not m: continue
        similars = 0
        for n in messages:
            if n and n[-1] == m[-1]:
                similars += 1
                if similars >= len(messages) / 2:
                    return m
    return []


def determine_common_suffix(messages, possible_suffix):
    ad, common_suffix = [], possible_suffix
    for m in messages:
        if m and m[-1] == common_suffix[-1]:
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