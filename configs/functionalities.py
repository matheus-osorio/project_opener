{'new': False, 'name': None, 'folder': None,
 'editor': None, 'edit': False, 'hash': None, 'list': False, 'delete': False, 
 'define': False, 'content': False, 'change_hash_length': None, 
 'change_standart_editor': None, 'change_stardart_folder': None, 'open': False}

functionalities = {
    'new_project': {
        'starter': 'new',
        'required': ['name','folder'],
        'optionals': ['editor','relative']
    },
    'edit_project':{
        'starter': 'edit',
        'required': ['hash'],
        'at_least': ['name','folder','editor','relative']
    },
    'list_projects':{
        'starter': 'list',
        'required': []
    },
    'delete_project':{
        'starter':'delete',
        'required': ['hash']
    },
    'define_variable':{
        'starter': 'define',
        'required':['name', 'content']
    },
    'change_hash_length':{
        'starter': 'change_hash_length',
        'required': ['content']
    },
    'change_standart_editor':{
        'starter': 'change_standart_editor',
        'required': ['content']
    },
    'change_stardart_folder':{
        'starter': 'change_stardart_folder',
        'required': ['content']
    },
    'open_project':{
        'starter': 'open',
        'at_least': ['name', 'hash']
    }
}