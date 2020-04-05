#!/usr/bin/env python2

import getopt, os, subprocess, sys

patchdir = os.path.dirname(os.path.realpath(__file__)) + '/../patches/'
if 'DESTDIR' in os.environ:
    winedir = os.environ['DESTDIR']
else:
    winedir = '.'
backend = "patch"

applied = []

def usage():
    print '''
Usage: ./staging/patchinstall.py [DESTDIR=path] [options] [patchset ...]

Applies every patch to a Wine tree.

Options:
    -h, --help          print this message
    --all               apply all patches (except those excluded with -W)
    -W <patchset>       exclude a patch
    --no-autoconf       do not run autoconf and tools/make_requests
    --backend=<backend> use the given backend to apply patches:
              patch     use the `gitapply.sh` tool (a wrapper around `patch`)
              git-am    use `git am`
              git-am-C1 use `git am -C1`
              git-apply use `git apply`
    -r, --rebase-mode   alias for --backend=git-am-C1 --no-autoconf
'''

# return a patch to be shoved in patchlist below
def parse_def_file(name, path):
    deps = []
    if os.path.exists(path):
        with open(path) as z:
            for l in z.readlines():
                if l.lower().startswith('depends: '):
                    deps.append(l.split(' ')[1].strip())
                elif l.lower().strip() == 'disabled: true':
                    return None
    return deps

def apply_patch(patch):
    if backend == 'git-am':
        return subprocess.call(['git','-C',winedir,'am',patch])
    elif backend == 'git-am-C1':
        return subprocess.call(['git','-C',winedir,'am','-C1',patch])
    elif backend == 'patch':
        with open(patch) as f:
            return subprocess.call([patchdir+'/gitapply.sh'],stdin=f)
    elif backend == 'git-apply':
        return subprocess.call(['git','-C',winedir,'apply','--index',patch])

def apply_set(patchlist, name):
    if name in applied:
        return True
    for dep in patchlist[name]:
        if not apply_set(patchlist, dep):
            return False
    print 'Applying',name
    for patch in sorted(os.listdir(patchdir+'/'+name)):
        if patch.endswith('.patch') and patch.startswith('0') and apply_patch(patchdir+'/'+name+'/'+patch):
            print 'Failed to apply patch %s/%s' %(name, patch)
            return False
    applied.append(name)
    return True

def add_patchset(patchlist, name):
    path = patchdir + '/' + name
    if os.path.isdir(path):
        deps = parse_def_file(name, path + '/definition')
        if deps == None:
            print 'Error: attempt to apply %s, but it is disabled.' %name
            sys.exit(1)
        patchlist[name] = deps
        for dep in deps: add_patchset(patchlist, dep)

def main():
    global backend
    patchlist = {}
    excluded = []
    no_autoconf = False
    force_autoconf = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hrW:', ['all', 'backend', 'help', 'no-autoconf'])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    for o, a in opts:
        if o == '-h' or o == '--help':
            usage()
            sys.exit(0)
        elif o == '-r' or o == '--rebase-mode':
            no_autoconf = True
            backend = "git-am-C1"
        elif o == '-W':
            excluded.append(a)
        elif o == '--all':
            for name in os.listdir(patchdir):
                path = patchdir + '/' + name
                if os.path.isdir(path):
                    deps = parse_def_file(name, path + '/definition')
                    if deps != None: # it's not disabled
                        patchlist[name] = deps
        elif o == '--backend':
            backend = a
        elif o == '--no-autoconf':
            no_autoconf = True

    for a in args: add_patchset(patchlist, a)

    for p in excluded: del patchlist[p]

    if not patchlist:
        print 'Error: no patches specified'
        sys.exit(1)

    # Check that all of our dependencies exist
    for p in patchlist:
        deps = patchlist[p]
        for d in deps:
            if d not in patchlist:
                print 'Error: unknown or disabled dependency %s of %s.' %(d,p)
                sys.exit(1)

    # Now try to apply each patch
    for p in sorted(patchlist.keys()):
        # Try to apply it
        if not apply_set(patchlist, p):
            sys.exit(1)

    # we successfully applied everything, autogen some files so we can build
    if not no_autoconf:
        print 'Calling autoreconf -f...'
        subprocess.call(['autoreconf','-f'],cwd=winedir)
        print 'Calling tools/make_requests...'
        subprocess.call(['./tools/make_requests'],cwd=winedir)
    sys.exit(0)

if __name__ == '__main__':
    main()
