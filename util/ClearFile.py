import os
import send2trash


class ClearFile:
    @staticmethod
    def clear():
        data_path_home = os.path.join(os.getcwd(), 'data', 'pages_home')
        data_path_bar = os.path.join(os.getcwd(), 'data', 'pages_bar')

        for filename in os.listdir(data_path_home):
            if filename.endswith('.txt'):
                send2trash.send2trash(os.path.join(data_path_home, filename))

        for filename in os.listdir(data_path_bar):
            if filename.endswith('.txt'):
                send2trash.send2trash(os.path.join(data_path_bar, filename))

