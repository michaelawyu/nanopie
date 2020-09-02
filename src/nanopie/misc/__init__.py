from typing import Dict


def get_flattenable_dikt(dikt: Dict) -> Dict:
    """"""
    result = {}

    for k in dikt:
        if type(dikt[k]) in [str, bool, int, float]:
            result[k] = dikt[k]
        elif type(dikt[k]) == list:
            flag = True
            for i in dikt[k]:
                if type(i) not in [str, bool, int, float]:
                    flag = False
                    break
            if flag:
                result[k] = dikt[k]

    return result


def format_error_message(message, **kwargs):
    """"""
    if kwargs:
        message = message + " " + str(kwargs)

    return message
