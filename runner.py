#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Wed Apr 25 17:00:25 2018
#========================================
import sys, os, subprocess
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

spliter = {'win32':';', 'linux2':':', 'darwin':':'}

class Runner(object):
    '''
    '''
    def __init__(self, batch_mode=False):
        '''
        '''
        self.__mode = batch_mode
        self.__env  = os.environ.copy()




    def put_env(self, name, value, mode='over'):
        '''
        '''
        if mode == 'over':
            self.__env[name] = value

        elif mode == 'pre':
            self.__env[name] = '{0}{1}{2}'.format(value, spliter.get(sys.platform, ':'), self.__env.get(name, ''))

        elif mode == 'post':
            self.__env[name] = '{0}{1}{2}'.format(self.__env.get(name, ''), spliter.get(sys.platform, ':'), value)




    def run(self, executable, *argments):
        '''
        '''
        _cmds = [executable]
        _cmds.extend(argments)
        if self.__mode:
            subprocess.check_call(_cmds, env=self.__env)
        else:
            subprocess.Popen(_cmds, env=self.__env)




if __name__ == '__main__':
    runner = Runner(batch_mode=True)
    runner.put_env('MAYA_UI_LANGUAGE', 'zh_CN')
    runner.run('C:/Program Files/Autodesk/Maya2017/bin/maya.exe')
