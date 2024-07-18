# this file is editable
# the originalfields are:
# username='', password='', group='', title='', url=''
# so for one to assign custom fields, one has to 
# define the custom fields in the key section of 
# the function mapperd


def mapperd (username='', password='', group='', title='', url=''):
    
    maps = {

        'organization'  : {'group': group}, 
        'repository'    : {'title': title}, 
        'username'      : {'username': username}, 
        'password'      : {'password': password},
        'database'      : {'url': url}
    }
    
    return maps