import json
import random
import Levenshtein as Lev
import configs.bcolors as bcolors
import os

colors = bcolors.bcolors()

class Organizer:
    
    def __init__(self,path):

        #json related code
        self.json_folder = path + '/configs/configs.json'
        f = open(self.json_folder)
        self.configs = json.loads(f.read())
        
        #sets some of the variables inside the json folder as class variables
        self.std_folder = self.configs['sys_definitions']['standart_folder']
        self.std_editor = self.configs['sys_definitions']['standart_editor']
        self.duplicate_policy = self.configs['sys_definitions']['duplicate_policy']
        self.hash_len = self.configs['sys_definitions']['hash_length']
        self.usr_definitions = self.configs['user_definitions']

        #creates object with hash as key and project as content
        projects = self.configs['projects']
        self.projects = {proj['hash']: proj for proj in projects}

        #starts the variables to be used later in replacement function
        self.variables = {}
        self.variables.update(self.configs['sys_definitions'])
        self.variables.update(self.configs['user_definitions'])
        
        #starts a variable with project name as key and project as content
        self.projects_names = {}
        for proj in projects:
            for name in proj['name']:
                if name in self.projects_names.keys():
                    print(f'WARNING: PROJECT NAME IS DEFINED TWICE. REPLACE POLICY IS SET TO {self.duplicate_policy}.')
                    if self.duplicate_policy == 'replace':
                        self.projects_names[name] = proj
                else:
                    self.projects_names[name] = proj

        #creates messages for different types of results
        self.messages = {
            'NO_HASH_FOUND': self.make_return_message(f'{colors.FAIL}ERROR{colors.ENDC}', 'The hash is not in the system. Please verify'),
            'ADDED_TO_PROJECT_LIST': self.make_return_message(f'{colors.OKBLUE}SUCESS{colors.ENDC}', 'The Project has been added to the list!'),
            'SUCCESSFULLY_DELETED': self.make_return_message(f'{colors.OKBLUE}SUCESS{colors.ENDC}', 'The project reference has been deleted!'),
            'FILE_EDITED_SUCESSFULLY': self.make_return_message(f'{colors.OKGREEN}SUCCESS{colors.ENDC}', 'The project has been edited successfully'),
            'DEFINED_VARIABLE': self.make_return_message(f'{colors.OKGREEN}SUCCESS{colors.ENDC}', 'The variable has been added'),
            'SYSTEM_VARIABLE_NOT_DEFINED': self.make_return_message(f'{colors.FAIL}ERROR{colors.ENDC}', 'System variables cannot be added, just edited.'),
            'SYSTEM_VARIABLE_EDITED': self.make_return_message(f'{colors.OKGREEN}SUCCESS{colors.ENDC}', 'The variable has been edited'),
            'NO_PROJECT_WITH_THIS_NAME': self.make_return_message(f'{colors.FAIL}ERROR{colors.ENDC}', 'There is no project with this name.'),
            'OPENING_PROJECT': self.make_return_message(f'{colors.OKGREEN}SUCCESS{colors.ENDC}', 'Project will be opened!'),
            'NO_HASH_AVAILABLE': self.make_return_message(f'{colors.FAIL}ERROR{colors.ENDC}', 'In over 1000 tries the system could not find a unique hash. You probably set the hash values too short.')
        }

    def create_hash(self):
        possibles = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM12345678901234567890'
        hashText = ''
        for _ in range(self.hash_len):
            hashText += random.choice(possibles)
        
        return hashText
    
    def new_project(self,name,folder,editor=None,run=[] ,absolute=False):

        print('entrou ',run)
        editor = '${standart_editor}' if editor == None else editor 
        
        if not absolute:
            folder = '${standart_folder}' + folder

        existing_hashes = self.projects.keys()

        count = 0
        while True:
            new_hash = self.create_hash()
            if new_hash not in existing_hashes:
                break
            else:
                count+=1
                if count > 1000:
                    return self.messages['NO_HASH_AVAILABLE']
        
        
        
        self.configs['projects'].append({
            'hash': new_hash,
            'name': name,
            'editor': editor,
            'folder': folder,
            'run': run
        }) 
        
        self.save_file()

        return self.messages['ADDED_TO_PROJECT_LIST']

    def edit_project(self,proj_hash,obj):
        if not self.hash_exists(proj_hash):
            return self.messages['NO_HASH_FOUND']


        if 'folder' in obj.keys():
            if  'absolute' not in obj.keys():
                obj['folder'] = '${standart_folder}' + obj['folder']
    
        self.projects[proj_hash].update(obj)

        self.save_file()
        return self.messages['FILE_EDITED_SUCESSFULLY']
    
    def list_projects(self):
        txt = ''' 
        
        LIST OF PROJECTS
        ---------------

        USER DEFINED VARIABLES:
        {}
        ---------------
        PROJECTS:
        {}
        '''
        user_def = [f'{colors.OKBLUE}{key}{colors.ENDC}: {colors.WARNING}{self.usr_definitions[key]}{colors.ENDC}' 
                    for key in self.usr_definitions.keys()]
        
        user_def = '\n\t'.join(user_def)

        projects = []

        for proj in self.projects.values():
            line = f'''
            hash:\t{colors.OKCYAN}{proj['hash']}{colors.ENDC}
            name:\t{colors.HEADER}{proj['name']}{colors.ENDC}
            folder:\t{colors.OKGREEN}{proj['folder']}{colors.ENDC}
            editor:\t{colors.WARNING}{proj['editor']}{colors.ENDC}
            run:\t{colors.OKBLUE}{proj['run']}{colors.ENDC}
            '''

            projects.append(line)
        
        projects = '\n-------\n'.join(projects)

        txt =  txt.format(user_def,projects)

        return {
            'type': 'MESSAGE',
            'text': txt
        }



    def delete_project(self,proj_hash):

        if not self.hash_exists(proj_hash):
            return self.messages['NO_HASH_FOUND']

        p = self.configs['projects']
        self.configs['projects'] = [proj for proj in p if proj['hash'] != proj_hash]
        self.save_file()

        return self.messages['SUCCESSFULLY_DELETED']


    def define_variable(self,variable,content):
        self.configs['user_definitions'][variable] = content
        self.save_file()

        return self.messages['DEFINED_VARIABLE']


    def change_sys_variable(self,variable,content):
        if variable not in self.configs['sys_definitions'].keys():
            return self.messages['SYSTEM_VARIABLE_NOT_DEFINED']
        
        self.configs['sys_definitions'][variable] = content
        self.save_file()

        return self.messages['SYSTEM_VARIABLE_EDITED']
    
    def open_project(self,name):
        difference = [Lev.distance(name.lower(),proj_name.lower()) for proj_name in self.projects_names.keys()]

        smallest = min(difference)
        smallest_index = difference.index(smallest)
        smallest_name = list(self.projects_names.keys())[smallest_index]
        if smallest > 2:
            choice = input(f'Did you mean {smallest_name}? Type [Y/N]')
            if choice.lower() != 'y':
                return self.messages['NO_PROJECT_WITH_THIS_NAME']
        
        project = self.projects_names[smallest_name]

        folder = project['folder']

        editor = project['editor']

        run = project['run']
        
        for var in self.variables.keys():
            folder = folder.replace('${' + var + '}', str(self.variables[var]))
            editor = editor.replace('${' + var + '}', str(self.variables[var]))
        
        os.system(f'cd {folder};{editor}')

        for command in run:
            os.system(f'cd {folder};{command}')

        return self.messages['OPENING_PROJECT']


        

    def hash_exists(self,proj_hash):
        return proj_hash in self.projects.keys()


    def make_return_message(self,msg_type,msg_text,additional_info = {}):
        msg = {
            'type': msg_type,
            'text': msg_text
        }
        msg.update(additional_info)
        return msg

    def save_file(self):
        f = open(self.json_folder,'w')
        try:
            parsed = json.dumps(self.configs)
        except SyntaxError:
            raise Exception('Syntax Error when trying to parse to json.')
        except:
            raise Exception('Something went wrong...')

        f.write(json.dumps(self.configs))



