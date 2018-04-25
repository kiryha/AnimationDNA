#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Wed Apr 25 17:00:25 2018
#========================================
import os, re, subprocess
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class Runner(object):
    '''
    '''
    def __init__(self):
        '''
        '''
        self.__env = os.environ.copy()




    def put_env(self, name, value, mode='over'):
        '''
        '''
        if mode == 'over':
            self.__env[name] = value

        elif mode == 'pre':
            self.__env[name] = '{0};{1}'.format(value, self.__env.get(name, ''))

        elif mode == 'post':
            self.__env[name] = '{0};{1}'.format(self.__env.get(name, '', value))




    def run(self, executable, *argments):
        '''
        '''
        _cmds = [executable]
        _cmds.extend(argments)
        subprocess.Popen(_cmds, env=self.__env)




if __name__ == '__main__':
    runner = Runner()
    runner.put_env('MAYA_UI_LANGUAGE', 'en_US')
    runner.run('C:/Program Files/Autodesk/Maya2017/bin/maya.exe')