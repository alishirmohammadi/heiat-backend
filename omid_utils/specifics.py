def check_melli_code(mellicode):
    a = mellicode
    if (len(a) == 8):
        a = '00' + a
    if (len(a) == 9):
        a = '0' + a
    if (len(a) == 10):
        r = 0
        for i in range(0, 9):
            r1 = int(a[i]) * (10 - i)
            r = r1 + r
        c = r % 11
        if (int(a[9]) == 1) and (c == 1):
            return True
        elif (int(a[9]) == 0) and (c == 0):
            return True
        elif (int(a[9]) == 11 - c):
            return True
        else:
            return False
    else:
        return False


def student_enterance(studentnumber):
    return studentnumber[0:2]


def student_type(studentnumber):
    a = studentnumber[2]
    if a == 1:
        type = 'bs'
    elif a == 2 or a == 7:
        type = 'ms'
    elif a == 3:
        type = 'phd'
    else:
        type = 'unkhown'
    return type
