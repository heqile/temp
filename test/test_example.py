import json

import pytest


class A(object):
    def __init__(self):
        pass

    def process(self):
        return "A"


class B(object):
    def __init__(self):
        pass

    def process(self, arg1):
        return arg1


class C(object):
    def __init__(self):
        pass

    def process(self, arg2):
        return arg2


with open("C:\\Users\\mrqil\\PycharmProjects\\testone\\test\\configuration.json", "r") as f:
    test_conf = json.load(f)


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for test_name, configurations in test_conf.items():
        idlist.append(test_name)
        argnames = "test_config"
        argvalues.append(configurations)
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


class TestMe(object):

    def test(self, test_config):
        func_list = list()
        for func_conf in test_config:
            if isinstance(func_conf, unicode):
                func_list.append({func_conf: None})
            elif isinstance(func_conf, dict):
                func_name = func_conf.keys()[0]
                func_args = func_conf.values()[0]
                if isinstance(func_args, list):
                    for args in func_args:
                        func_list.append({func_name: args})
                else:
                    func_list.append({func_name: func_args})

        for func in func_list:
            func_instance = globals()[func.keys()[0]]()
            for key, value in func.items():
                if value is None:
                    func_instance.process()
                elif isinstance(value, list):
                    for item in value:
                        func_instance.process(**item)
                else:
                    func_instance.process(**value)

