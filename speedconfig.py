#! /bin/python
import sys

args = sys.argv[1:]

class PObject:
    filename = ''
    hosts = ''
    service = ''
    configs = []
    def configure(t, filepath, configpath, backup):
        f = open(filepath, 'r')
        t.configs = f.read().splitlines()
        f.close()
        iterconf = iter(t.configs)
        try:
            namedef = iterconf.next()
        except AttributeError:
            namedef = iterconf.__next__()
        f = open(t.filename, 'w+')
        print('Adding configs from ' + filepath)

        f.write('---\n  - name: '+ namedef +'\n    tasks:\n')
        if(backup == 'd'):
            f.write(' '*6+'- name: Backing up '+configpath+'\n        copy:\n          src: "'+configpath+'"\n          dest: "/tmp'+configpath+'_backup"\n          backup: yes\n')
        else:
            f.write('      - name: Finding path of '+configpath+' file\n        find:\n          paths: '+backup+'\n          recurse: yes\n          patterns: "'+configpath+'"\n        register: files_matched\n')
            f.write(' '*6+'- name: Backing up '+backup+'\n        copy:\n          src: "{{ files_matched.files[0].path }}"\n          dest: "/tmp'+backup+'_backup"\n          backup: yes\n')
            configpath = '{{ files_matched.files[0].path }}'
        configDump = ''
        count = 0
        for config in iterconf:
            count += 1
            configDump += t.configFormat(config, count, configpath)
        f.write(configDump)
        f.close()
        print('Done with '+t.filename)

    def ssh(t, config, count, configpath): 
        header = ' '*6+'- name: '+config+' ['+str(count)+'/'+str(len(t.configs)-1)+']\n' 
        body = ' '*8+'linefile:\n'+' '*10+'dest: \"'+configpath+'\"\n'+' '*10+'regexp: \"^'+config[0:config.index(' ')]+'\"\n'+' '*10+'line: \"'+config+'\"\n' 
        return header + body 
    def php(t, config, count, configpath):
        header = ' '*6+'- name: '+config+' ['+str(count)+'/'+str(len(t.configs)-1)+']\n' 
        body = '' 
        return header + body 
    def configFormat(t, config, count, configPath):
        switcher = {
                0: t.ssh, 
                1: t.php,
                }
        return switcher[int(t.service)](config, count, configPath)
        
def newPObject(filename, hosts, service):
    f = open(filename, 'w+')
    f.close()
    pObject = PObject()
    pObject.filename = filename
    pObject.hosts = hosts
    pObject.service = service
    return pObject

def main():
    if(len(args) == 10 or len(args) == 12): 
        count = 0
        recursivepath = 'no'
        for option in args:
            if(count % 2 == 0):
                if(args[count] == '-f'):
                    filename = args[count+1]
                elif(args[count] == '-g'):
                    hosts = args[count+1]
                elif(args[count] == '-s'):
                    service = int(args[count+1])
                elif(args[count] == '-i'):
                    infile = args[count+1]
                elif(args[count] == '-d'):
                    destfile = args[count+1]
                elif(args[count] == '-r'):
                    recursivepath = args[count+1]
            count += 1
        print('infile: '+infile)
        f = newPObject(filename, hosts, service)
        if recursivepath == 'no':
            f.configure(infile, destfile, 'd')
        else:
            f.configure(infile, destfile, recursivepath)
    else:
        print('not enoguh args owo')
main()