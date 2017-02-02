
import os
import re
import sys
import argparse
import subprocess

basename = 'synapse_dockerfile'
re_tag = re.compile('ENV SYN_GIT_TAG .*\n')
repo_url = 'https://github.com/vertexproject/synapse.git'

def getTags():
    ret = subprocess.check_output(['git', 'ls-remote', '--tags', '--refs', repo_url, 'v*'])
    ret = ret.decode('utf-8')
    tags = []
    for line in ret.splitlines():
        tags.append(line.rsplit('/')[-1])
    return tags

def main(argv):
    if __file__ not in os.listdir('.'):
        raise Exception('run this from the directory it\'s in')
    
    syn_path = os.path.join('latest', basename)
    with open(syn_path, 'r') as fd:
        syn_docker_buf = fd.read()

    for tag in getTags():
        path = os.path.join(tag, basename)
        repl = 'ENV SYN_GIT_TAG %s\n' % (tag,)

        os.makedirs(tag, exist_ok=True)
        buf = re_tag.sub(repl, syn_docker_buf)
        with open(path, 'w') as fd:
            print('writing: %r' % (path,))
            fd.write(buf)
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
