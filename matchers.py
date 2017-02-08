from hamcrest.core.base_matcher import BaseMatcher


class HasAttributes(BaseMatcher):

    """
    http://test.loc/schema/test_schema.xsd
    """

    text1 = u' количество атрибутов <%s>'
    text2 = u' не найден атрибут <%s>'

    def __init__(self, attributes_list):
        self.attributes_list = attributes_list
        self.expected = None
        self.actual = None

    def _matches(self, item):
        if len(item.__dict__) != len(self.attributes_list):
            self.expected = self.text1 % str(len(self.attributes_list))
            self.actual = self.text1 % str(len(item.__dict__))
            return False
        else:
            for a in self.attributes_list:
                if not hasattr(item, a):
                    self.expected = self.text2 % str(a)
                    self.actual = None
                    return False
            return True

    def describe_to(self, description):
        description.append_text(self.expected)

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_description_of(self.actual)


def has_attributes(attributes_list):
    return HasAttributes(attributes_list)


class ComparesAttributes(BaseMatcher):

    def __init__(self, expected_attributes):
        self.expected_attributes = expected_attributes
        self.expected_text = None
        self.actual_text = None

    def _matches(self, item):
        for key, value in item.__dict__.items():
            try:
                expected_attribute = getattr(self.expected_attributes, key)
                if expected_attribute is None:  # заменяет None из DAO на пустую строку как в soap ответе
                    expected_attribute = ''
                if str(expected_attribute) != str(value):
                    self.expected_text = "атрибут " + key + " = " + str(expected_attribute)
                    self.actual_text = "атрибут " + key + " = " + str(value)
                    return False
            except AttributeError:
                pass
        return True

    def describe_to(self, description):
        description.append_text(self.expected_text)

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_description_of(self.actual_text)


def compares_attributes(attributes):
    return ComparesAttributes(attributes)
