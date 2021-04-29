#!/usr/bin/env python3

import json
import argparse as ap
import sys
from Validator import Validator
from Control import Control


path = sys.path[0]

parser = ap.ArgumentParser(allow_abbrev=False)

# args to make a new config
parser.add_argument('-n','--new',required=False, action='store_true', help='Sets mode to new. Use with -na(name), -f(folder)[OPTIONAL] and -ed(editor)[OPTIONAL]') # category arg
parser.add_argument('-na','--name',required=False, nargs='+') # name arg
parser.add_argument('-f','--folder',type=str,required=False) # folder arg
parser.add_argument('-ed','--editor',type=str,required=False) # editor arg
parser.add_argument('--absolute',required=False,action='store_true')

# args to edit 
# edit uses basically the same patterns as new, so i'm not reddefinig the arguments
parser.add_argument('-e','--edit',required=False,action='store_true') #category arg
parser.add_argument('-ha', '--hash',type=str,required=False) #hash arg

# list of your opening configurations
parser.add_argument('-l','--list',required=False,action='store_true') # category arg

#delete statement
#uses hash to delete
parser.add_argument('-del','--delete',required=False,action='store_true') # category arg


# define variables
parser.add_argument('-def','--define',required=False,action='store_true') #category arg
parser.add_argument('-con','--content', required=False) #category arg

#change system variables
parser.add_argument('--change-hash-length',required=False,action='store_true')
parser.add_argument('--change-standart-editor',required=False,action='store_true')
parser.add_argument('--change-standart-folder',required=False,action='store_true')
parser.add_argument('--change-replacement-policy',required=False,action='store_true')

#open projects
parser.add_argument('-o','--open', required=False,action='store_true')

args = vars(parser.parse_args())

validator = Validator(args)

control = Control()

control.run(validator.get_params(),path)



