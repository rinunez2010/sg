import re

SOH = chr(1)
FIX42TAGS = ["8", "35", "55", "54", "38", "40", "59", "167", "1", "44"]
T54_VALUES = ['1', '2']
T54_MEANING = {'1': "bought", '2': "sold"}
T40_VALUES = ['1', '2', '3', '4', '5']
T59_VALUES = ['0', '1', '2', '3', '4', '5', '6']
T167_VALUES = ['FUT', 'OPT', 'CS']


class FixObject:
    """"
    Class which will has all of the fix 4.2 object states and methods
    """

    def __init__(self, t55n, t54, t38n, t40, t59, t167, t1n, t44f):
        """Check if the parameters pass the constraints

        Parameter names which end with an n, type is int
        Parameter names which end with an f, type is float"""
        if not isinstance(t55n, int) or t55n < 1:
            raise AttributeError("SYMBOL_N not valid. N should be a number >=1")
        if t54 not in T54_VALUES:
            raise AttributeError("54 doesn't have valid values")
        if not isinstance(t38n, int) or t38n < 1:
            raise AttributeError("38 should be a positive integer")
        if t40 not in T40_VALUES:
            raise AttributeError("40 doesn't have valid values")
        if t59 not in T59_VALUES:
            raise AttributeError("59 doesn't have valid values")
        if t167 not in T167_VALUES:
            raise AttributeError("167 doesn't have valid values")
        if not isinstance(t1n, int) or t1n < 1:
            raise AttributeError("CLIENT_N not valid. N should be an integer number >=1")
        if not isinstance(t44f, float) or t44f <= 0:
            raise AttributeError("440 should be an positive float number")

        self.t55 = "SYMBOL_" + str(t55n)
        self.t54 = t54
        self.t38 = str(t38n)
        self.t40 = t40
        self.t59 = t59
        self.t167 = t167
        self.t1 = "CLIENT_" + str(t1n)
        self.t44 = str(t44f)

    def get_fix_message(self):
        """"Return the fix 4.2 message"""
        message = "8=FIX.4.2" + SOH + \
                  "35=D" + SOH + \
                  "55=" + self.t55 + SOH + \
                  "54=" + self.t54 + SOH + \
                  "38=" + self.t38 + SOH + \
                  "40=" + self.t40 + SOH + \
                  "59=" + self.t59 + SOH + \
                  "167=" + self.t167 + SOH + \
                  "1=" + self.t1 + SOH + \
                  "44=" + self.t44
        return message

    def get_fix_instance(message):
        """"fix 4.2 message -> FixObject

        This is a static method to get a FixObject from a fix 4.2 message.
        Tags which finish with s will have to be type converted
        """
        tag_values = message.split(SOH)
        tags = {}
        for tag_value in tag_values:
            (tag, value) = tag_value.split("=")
            tags[tag] = value
        tag_keys = tags.keys()
        for i in tag_keys:
            if i not in FIX42TAGS:
                raise AttributeError("Tag " + i + " in message (" + message +
                                     ") is not FIX 4.2 compliant")
        # Let's check what is not checked at the __init__ method
        for i in FIX42TAGS:
            if i not in tag_keys:
                raise AttributeError("Tag " + i + " missing in message " + message)
            if i == "8" and tags[i] != "FIX.4.2":
                raise AttributeError("Tag 8 should be 'FIX.4.2'")
            if i == "35" and tags[i] != "D":
                raise AttributeError("Tag 35 should be 'D'")
            if i == "55":
                p = re.compile(r'^SYMBOL_(\d+)$')
                m = p.match(tags[i])
                if not m:
                    raise AttributeError("Tag 55 should be like 'SYMBOL_N'")
                t55s = m.group(1)
            if i == "1":
                p = re.compile(r'^CLIENT_(\d+)$')
                m = p.match(tags[i])
                if not m:
                    raise AttributeError("Tag 1 should be like 'CLIENT_N'")
                t1s = m.group(1)
        return FixObject(int(t55s),
                         tags['54'],
                         int(tags['38']),
                         tags['40'],
                         tags['59'],
                         tags['167'],
                         int(t1s),
                         float(tags['44']))

    get_fix_instance = staticmethod(get_fix_instance)
