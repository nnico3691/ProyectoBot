from datetime import datetime


class Archivo:

    def Write(Value,URL):

        with open(URL, "a") as file_object:
            file_object.write(Value + "\n")
