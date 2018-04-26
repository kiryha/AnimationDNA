#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Wed Apr 25 18:09:05 2018
#========================================
import sys
import yaml, fire
import runner
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def launch(exe, batch_mode=False, config='', env='', args=''):
    '''
    --batch-mode
    --config       /path/to/config.yaml
    --env          name*value|name*value*mode;
    --args         -x | -xx | -xxx ...
    Exp:
        launcher.py launch --exe="Nuke10.0.exe" --batch-mode --env="NUKE_PATH*C:/" --args="--nukex"
    '''
    #- initialize app runner.
    _runner = runner.Runner(batch_mode)

    #- parse config file
    #- 
    #- 

    #- setting environments
    for e in env.split('|'):
        if e.count('*') == 1:
            en, ev = e.split('*')
            em = 'over'
        elif e.count('*') == 2:
            en, ev, em = e.split('*')
        else:
            sys.stdout.write('Can not parse enviroment variable - {0}\n'.format(e))
            continue
        _runner.put_env(en, ev, em)

    #- open software
    _runner.run(exe, *args.split('|'))




if __name__ == '__main__':
    fire.Fire({'launch':launch})
