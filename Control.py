from configs.Organizer import Organizer



class Control:
    def run(self,obj):
        st = obj['starter']
        self.Organizer = Organizer()
        response = self[st](obj)

        txt = f''' 
        RESPONSE TYPE: {response['type']}
        
        --------------

        RESPONSE MESSAGE: {response['text']}

        '''

        print(txt)

    
    def new(self,obj):
        return self.Organizer.new_project(**obj['params'])

    def edit(self,obj):
        params = obj['params']
        proj_hash = params['hash']
        del params['hash']
        return self.Organizer.edit_project(proj_hash,obj['params'])

    def list(self,obj):
        return self.Organizer.list_projects()

    def delete(self,obj):

        return self.Organizer.delete_project(obj['params']['hash'])

    def define(self,obj):
        params = obj['params']
        name = params['name'][0]
        content = params['content']
        return self.Organizer.define_variable(name,content)

    def change_hash_length(self,obj):
        pass

    def change_stardart_folder(self,obj):
        pass

    def change_standart_editor(self,obj):
        pass

    def change_replacement_policy(self,obj):
        pass

    def open(self,obj):
        name = obj['params']['name'][0]
        return self.Organizer.open_project(name)
    
    def __getitem__(self,attr):
        return self.__getattribute__(attr)
    
