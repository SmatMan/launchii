import os


class OSXOpen:
    @staticmethod
    def supported_environment(platform: str):
        return platform == "Darwin"

    def do(self, target):
        return os.system("open " + target)


class WindowsOpen:
    @staticmethod
    def supported_environment(platform: str):
        return platform == "Windows"

    def do(self, target):
        return os.startfile(target)
