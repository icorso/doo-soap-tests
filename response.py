import sys

from lxml import objectify


class Response:
    def __init__(self, text):
        self.__text = text
        self.__soap_object = None
        self.__xml = None

        try:
            self.__xml = self.__text.replace("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "")
            self.__soap_object = objectify.fromstring(self.__xml)
            self.__dict__.update(self.__soap_object.__dict__)
        except ValueError as err:
            print("Ошибка обработки данных от веб-сервиса :\n" + str(err))
        except:
            print("Системная ошибка :\n", sys.exc_info()[0])
            raise

    def __str__(self):
        return self.__xml
