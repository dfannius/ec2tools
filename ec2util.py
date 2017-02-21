# To do:
#  - make pem file configurable
#  - automatic variable substitution in run_cmd
#  - setting local and remote dirs

import os.path
import subprocess

def var_to_file( varname ):
    return os.path.expanduser( "~/.ec2/{}".format( varname.replace( "_", "-" ) ) )

def write_var( varname, val ):
    with open( var_to_file( varname ), 'w' ) as f:
        f.write( val )
        f.write( "\n" )

def read_var( varname ):
    with open( var_to_file( varname ), 'r' ) as f:
        val = f.readline()
        return val[:-1]

def write_ip( val ): write_var( "ip", val )
def write_user( val ): write_var( "user", val )

def read_ip(): return read_var( "ip" )
def read_user(): return read_var( "user" )
def read_local_dir(): return os.path.expanduser( read_var( "local-dir" ) )
def read_remote_dir(): return read_var( "remote-dir" )

def pem_file():
    return os.path.expanduser( "~/.ec2-credentials/kp1.pem" )

# Well, half-smart
# Attempts to keep double-quoted strings as a unit (but strips the double quotes)
# For use in passing command-line strings to shells
def smart_split( s ):
    q_start = s.find( '"' )
    if q_start != -1:
        q_end = s.find( '"', q_start + 1 )
        assert q_end != -1
        return s[:q_start].split() + [ s[q_start+1:q_end] ] + smart_split( s[q_end+1:] )
    else:
        return s.split()

def run_cmd( cmd ):
    subprocess.call( smart_split( cmd ) )
