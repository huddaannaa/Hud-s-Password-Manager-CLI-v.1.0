from Enginehud.util import key_from_keyfile
from Enginehud.db import Database
from mapper import mapperd
import platform
import argparse
import getpass
import string
import random
import signal
import uuid 
import time
import ast
import re
import sys
import os




class readers(object):
    """
    # the format of the file input shpould be as below:
    # key = value
    """
    def __init__(self, file_):
        self.file_ = file_
        
        
    def writer(self, data):f = open('{0}'.format(self.file_), "a+");f.write('{}\n'.format(data));f.close()
    def check_n_write (self, data):
        if os.path.exists(self.file_):os.utime(self.file_, None)
        else:self.writer(data)
    
    def reader(self): f=open(self.file_, 'rt'); return [n.strip('\n') for n in f.readlines()];f.close()    
    def file_to_dict(self):
        # print self.reader()
        ans = {}
        for k in self.reader():
            #print ("+++++++++")
            #print k
            if re.findall(r'^#',k): pass
            elif len(k) == 0: pass
            else:
                try:
                    ans[k.split('=')[0].strip()] = k.split('=')[1].strip()
                except:pass#print k
        return ans



def param_data(tr):

    param_datax="""#THE NAME OF THE DATABASE

name_of_database             = {0}_db.kdb
system_path                  =

#SPECIFY IF KEY/PASSPHRASE

use_encryption_key           = True
master_key_size              = 10246
master_key_file_name         = {0}_master-key.key
master_pass_file_name        = {0}_master-pass.ini""".format(tr)
    return param_datax



pce = argparse.ArgumentParser(description="""

Huds Password Manager for Automations

The application stores the fields below as inputs:
NOTE: The fields below are defaults and can be change by remapping
      them in mapper.py

#organization
#repository
#username
#password
#database

The application bares a cli interface where a given user can input
and view stored data. Data (Credentials) are stored in an encrypted database

""")
pce.add_argument('-c', '--config', type=str, metavar='', required=False, help='Specify a config file that exist, hence if not exist app will generate one based on the name you supplied, file must be of type [.ini], e.g **/root/hud/home/tuner.ini**')
args= pce.parse_args()

    


class authpack():

    def __init__(self, filex_='tuner.ini' ):
     
        #try:        # if filex is specified as arg
        if args.config: 
            filex_ = os.path.join(args.config)
            ini = os.path.basename(filex_)
            if len(re.findall(r'\.ini$', ini)) != 0:
                filex_ = os.path.join(args.config)
                
                # check is config file exists, if not create one
                if os.path.exists(filex_):
                    print ("")
                    print ("[+] A configuration file exists of some sort. hence the application will use that ..., ")
                    print ("[]>>>>>>")
                    print ("")
                    time.sleep(1)
                else:
                    print ("")
                    print ("[+] The specified configuration file does not exist, hence the application will create one ..")
                    print ("    with default settings ...")
                    time.sleep(1)
           
            else:
                print ("")
                print ("[+] settings file format should be of type [.ini]")
                print ("")
                sys.exit(0)

        #except:pass
            
        if filex_=='tuner.ini':
            print ("")
            print ("[+] use ** python -B .\control_panel_.py --help** and follow the instruction ")
            print ("")
            sys.exit(0)
        
        get_base_path = os.path.basename(filex_)
        get_name_of_file = param_data(re.findall(r'\w+', get_base_path)[0])
        #print data_
        settz = readers(filex_)
        settz.check_n_write(get_name_of_file)
        params = settz.file_to_dict()
               
        # THE NAME OF THE DATABASE
        self.db_file     =  params['name_of_database']
        system_path      =  params['system_path']
        
        # SPECIFY IF KEY/PASSPHRASE
        self.is_key      =  ast.literal_eval((params['use_encryption_key']))
        self.size_       =  int(params['master_key_size'])
        master_file_k_   =  params['master_key_file_name']
        master_file_p_   =  params['master_pass_file_name']
        
        # print bool(params['use_encryption_key'])
        # STATIC FIELDS
        self.log_file    = 'key-mngnt-reporter.log'
        self.vault       = '.huds_mngnt_vault'
    
        self.timer       =  str(time.asctime(time.localtime(time.time())))
        # print self.is_key
        # SYSTEM PATH
        if system_path:self.system_path = system_path
        else: self.system_path = '.' #os.path.expanduser("~")
        
        # KEY/PASSPHRASE
        if self.is_key == True:self.master_file = master_file_k_
        elif self.is_key == False:self.master_file = master_file_p_
        else:pass
        # for static or dynamic working directory assignment                      
        self.db_path     = os.path.join(self.system_path, self.vault, self.db_file)
        self.master_path = os.path.join(self.system_path, self.vault,  self.master_file)
        self.log_path    = os.path.join(self.system_path, self.vault,  self.log_file)        
        try:os.makedirs(os.path.join(self.system_path, self.vault))
        except:pass
        self.banner="""

  ____            _             _   ____                  _
 / ___|___  _ __ | |_ _ __ ___ | | |  _ \ __ _ _ __   ___| |
| |   / _ \| '_ \| __| '__/ _ \| | | |_) / _` | '_ \ / _ \ |
| |__| (_) | | | | |_| | | (_) | | |  __/ (_| | | | |  __/ |  _
 \____\___/|_| |_|\__|_|  \___/|_| |_|   \__,_|_| |_|\___|_| (_)
  
  
    Password (Credential) database management system
    built specifically for automations & integrations.
    
    (HKPM)
  
    Designed by 
    Hud Seidu Daannaa
  
    ==========

"""        
               
    def log(self, datax, show_timer=True):
        if show_timer == True:
            data = "{0} {1}".format(self.timer, datax)
            f = open('{0}'.format(self.log_path), "a+")
            f.write('{}\n'.format(data))
            f.close()
        else:
            data = "{0}".format(datax)
            f = open('{0}'.format(self.log_path), "a+")
            f.write('{}\n'.format(data))
            f.close()
        
        
    def read(self, file_): f=open(file_, 'rt'); return [n.strip('\n') for n in f.readlines()];f.close()    
    
    
    def write(self, file_1, data): 
        f = open('{0}'.format(file_1), "a+")
        f.write('{}\n'.format(data))
        f.close()

    
    def key_gen(self): return os.urandom(self.size_)
    
     
    def generate(self):    
        # the first output is lower and the second is upper
        o = """ZBTibm4t6tJ9qMWxrpMEk2k32WOz4Nu4YMx2zFza1vT0RjW12aDB828H2YohAPIXIw
fWBdnoCfZBTibm4t6tJ9qMWxrpMEk2k32WOz4Nu4YMx2zFza1vT0RjW12aDB828H2Yota3aKqakJe9jx0
MKHSoU5tu7CBDpMgTWh1o60tI47L94eymc8OipHLboy03JSQdTHimkTpUSd2VtkDWhDN3LdmV6oKFr8P9
QE0AoSjkx9nustTByt62HqvsDfp67zLZQ5VZBTibm4t6tJ9qMWxrpMEk2k32WOz4Nu4YMx2zFza1vT0Rj
W12aDB828H2YohAPIXIwfWBdnoCfZBTibm4t6tJ9qMWxrpMEk2k32WOz4Nu4YMx2zFza1vT0RjW12aDB8
28H2Yota3aKqakJe9jx0MKHSoU5tu7CBDpMgTWh1o60tI47L94eymc8OipHLboy03JSQdTHimkTpUSd2V
tkDWhDN3LdmV6oKFr8P9QE0AoSjkx9nustTByt62HqvsDfp67zLZQ5V"""
        def random_numbers(ln):
            d=''
            for x in range(len(str(ln))):
                d = d+str(random.randint(1,9))
            return d
        def random_block_letters(lnx):
            dx=''
            for x in range(len(str(lnx))):
                dx = dx + random.choice([n for n in string.ascii_uppercase])
            return dx    
        wrd=''
        for i in o:
            try:wrd=wrd+random_numbers(int(i))
            except ValueError:wrd=wrd+random_block_letters(str(i))
        return wrd.lower(), wrd.upper()

    
    def generate_roup(self):    
        # the first output is lower and the second is upper
        o = "HudDaann"
        def random_numbers(ln):
            d=''
            for x in range(len(str(ln))):
                d = d+str(random.randint(1,9))
            return d
        def random_block_letters(lnx):
            dx=''
            for x in range(len(str(lnx))):
                dx = dx + random.choice([n for n in string.ascii_uppercase])
            return dx    
        wrd=''
        for i in o:
            try:wrd=wrd+random_numbers(int(i))
            except ValueError:wrd=wrd+random_block_letters(str(i))
        return wrd.lower()
    
    
    def master_key(self):
        try:
            if self.is_key == False:
                # environment
                try:
                    os.environ.get('MASTER_PASS')
                    self.log ("[+] [IGNORE] this message if not applicable/Master-pass can be deleted ...")
                    key = os.environ.get('MASTER_PASS')
                    self.log ("[+] passwd success")
                    #print key
                    return key
                except:
                    # from file
                    #print 'xxxx'
                    if os.path.exists(self.master_path):
                        key = self.read(self.master_path)[0]
                        return key
                    else:               
                        self.write(self.master_path, str(self.generate()[1]))
                        self.log ("[+] Master file for pass does not exist")
                        self.log ("[>>>>] file will be created and master-pass will be generated ...")
                        self.log ("       NOTE: this new master-pass should be registered with the DB")
                        key = self.read(self.master_path)[0]
                        self.log ("[+] Master-pass generated successfully ... ")
                        self.log ("")
                        return key
                finally:
                    # from file
                    #print 'xxxx'
                    if os.path.exists(self.master_path):
                        key = self.read(self.master_path)[0]
                        return key
                    else:               
                        self.write(self.master_path, str(self.generate()[1]))
                        self.log ("[+] Master file for pass does not exist")
                        self.log ("[>>>>] file will be created and master-pass will be generated ...")
                        self.log ("       NOTE: this new master-pass should be registered with the DB")
                        key = self.read(self.master_path)[0]
                        self.log ("[+] Master-pass generated successfully ... ")
                        self.log ("")
                        return key
                        
            elif self.is_key == True:
                # environment
                try: 
                    os.environ.get('MASTER_KEY')           
                    self.log ("")
                    key = key_from_keyfile(os.environ.get('MASTER_KEY'))
                    self.log ("[+] key success")
                    return key
                except: # Exception as e:
                    #print e
                    # from file                
                    if os.path.exists(self.master_path):
                        key = key_from_keyfile(self.master_path)
                        return key
                    else:               
                        self.write(self.master_path, self.key_gen())
                        self.log ("[+] Master file for key not does exist")
                        self.log ("[>>>>] file will be created and master-key will be generated ...")
                        self.log ("       NOTE: this new master-key should be registered with the DB")
                        key = key_from_keyfile(self.master_path)
                        self.log ("[+] Master-key generated successfully ... ")
                        self.log ("")
                        return key
                finally: # Exception as e:
                    #print e
                    # from file                
                    if os.path.exists(self.master_path):
                        key = key_from_keyfile(self.master_path)
                        return key
                    else:               
                        self.write(self.master_path, self.key_gen())
                        self.log ("[+] Master file for key not does exist")
                        self.log ("[>>>>] file will be created and master-key will be generated ...")
                        self.log ("       NOTE: this new master-key should be registered with the DB")
                        key = key_from_keyfile(self.master_path)
                        self.log ("[+] Master-key generated successfully ... ")
                        self.log ("")
                        return key
            else: 
                self.log ("[+] [WARNING] System auth-type takes a boolean True/False")
                sys.exit(0)
                
        except Exception as err:
            self.log ("[+] [Master-key/pass function]")
            self.log ("[+] Could not create ")
            self.log (err)
            self.log ("")
            sys.exit(0)
                       
                       
    def get_pass(self, field_name):
    
        try:
            "get password and validate"
            while True:

                print ("")
                print ("[+] This field is mandatory [REQUIRED]")
                password1 = str(getpass.getpass('    Enter {} : '.format(field_name)))
                if len(password1) != 0:

                    print ("")
                    print ("[+] Verify field [REQUIRED]")
                    password2 = str(getpass.getpass('    Enter {} : '.format(field_name)))

                    if password1 == password2:
                        print ("")
                        print ("[+] Verified !")
                        return password1
                        break
                    else:
                        print ("")
                        print ("[+] Passwords [DO NOT MATCH]")
                        print ("[+] Please cross reference and retype the phrases")

                else:
                    print ("")
                    print ("[+] Password Field cannot be EMPTY")
                    print ("[+] Please cross reference and retype the phrases")
                    continue
        except Exception as err:
            print ("")
            print "[+] Password entry interrupted"
            self.log ("")
            self.log (err)
            self.log ("")


    def mapperx (self, username='', password='', group='', title='', url=''):

        mp = mapperd(username, password, group, title, url)


        def mx(maps):

            new_keys_to_values = {

                maps.keys()[0] : maps.values()[0].values()[0],
                maps.keys()[1] : maps.values()[1].values()[0],
                maps.keys()[2] : maps.values()[2].values()[0],
                maps.keys()[3] : maps.values()[3].values()[0],
                maps.keys()[4] : maps.values()[4].values()[0]
            }    
            old_keys_to_new_keys = {

                maps.keys()[0] : maps.values()[0].keys()[0],
                maps.keys()[1] : maps.values()[1].keys()[0],
                maps.keys()[2] : maps.values()[2].keys()[0],
                maps.keys()[3] : maps.values()[3].keys()[0],
                maps.keys()[4] : maps.values()[4].keys()[0]
            }    
            nn={}
            for n in maps.values():
                nn[n.keys()[0]] = n.values()[0]
            old_keys_to_values = nn

            return new_keys_to_values, old_keys_to_new_keys, old_keys_to_values
        
        ws = mx(mp)
        return ws

            
    def tabla(self, title=["index", "org", "group"], fields=[]):
        
        template = "    |{0:6}|{1:30}|{2:30}|"
        
        print ("     ______ ______________________________ _______________________________")
        #please for every increment in title=["index", "org", "group"], add a title[n]
        #below:
        print template.format(title[0], title[1], title[2])
        print ("     ------ ------------------------------ -------------------------------")
                              
        for rec in fields:
                              
            print template.format(*rec)
            print ("     ------ ------------------------------ -------------------------------")
    
               
    def db_(self):
        try:
            if os.path.exists(self.db_path):
                dbn = self.db_path         
                return dbn
            else:
                self.log ("[+] DB file does not exist")
                self.log ("[+] The Huds app, will now create a DB")
                self.log ("    and register it with the newly generated master-key")
                          
                dbx = Database()
                dbx.create_default_group()
                if self.is_key == False:
                    dbx.save(self.db_path, password=self.master_key())
                else:
                    dbx.save(self.db_path, self.master_key())
                dbn = self.db_path
                
                self.log ("[+] DB created successfully ... ")
                self.log ("")
                self.log ("\===============")
                self.log ("\[%] Since the database is newly created, the app will exit")
                self.log ("\    for the database to be populated with the require credentials ..")
                self.log ("\======")
                time.sleep(1)
                sys.exit(0)
        except Exception as err:
            self.log ("[+] [Db initialization function]")
            self.log ("[+] Could not initialize ")
            self.log ("    If DB exists it could be empty.. ")
            self.log (err)
            self.log ("")
            sys.exit(0)
            

    def get_base(self):
        
        ms_k = self.master_key()
        dbq = self.db_()
        
        try:
            if self.is_key == False:
                db = Database(dbq, password = ms_k)
                return db
            else:
                db = Database(dbq, ms_k)
                return db
        except Exception as err:
            self.log ("[+] [Db connection function]")
            self.log ("[+] Could not connect to DB ")
            self.log ("    If DB exists it could be empty.. ")
            self.log (err)
            self.log ("")
            sys.exit(0)

               
    def write_entries_to_db(self, username, password, group, title, url):
        try:           
            db = self.get_base()
            
            group = db.create_group(title=group.strip(), icon=1)
            group.create_entry(title=title.strip(), url=url.strip(), username=username.strip(), password=password.strip())
            
            if self.is_key == False:
                db.save(self.db_(), password=self.master_key())
            else:
                db.save(self.db_(), self.master_key())
            self.log ("[+] Written: {} was successful".format(title))
            return True
            
        except Exception as err:
            self.log ("[+] [Writing function]")
            self.log ("[+] Could not write the specific query into the db")
            self.log (err)
            self.log ("")
            
            sys.exit (0) 


    def delete_entries_in_db(self, groupx):
        print ("")
        try:       
            db = self.get_base()
            
            lett=[]
            for nrt in db.groups:            
                grp_match =  str(re.findall(r'title=\b\w+\b', str(nrt))[0].split('=')[1])                
                if grp_match == groupx:
                    self.log ("[+] {} exists".format(groupx))
                    lett.append(nrt)
                else:pass
           
            if len(lett) == 0:
                print ("[+] Input is either INVALID or EMPTY !i!i")
                print ("[+] Goto option <0> and view groups") 
                print ("    and specify a valid input")
               
                print ("")
                
            else:
                for nrt in lett:
                    print ("[+] Removing: {}".format(groupx))
                    self.log ("[+] Removing: {}".format(groupx))
                    nrt.remove()                
                    if self.is_key == False:
                        db.save(self.db_(), password=self.master_key())
                    else:
                        db.save(self.db_(), self.master_key())
                    print ("[+] Deleted: {} was successful".format(groupx))
                    self.log ("[+] Deleted: {} was successful".format(groupx))
                                
            return True            
        except Exception as err:
            self.log ("[+] [Deletion function]")
            self.log ("[+] Could not delete the specific query into the db")
            self.log (err)
            self.log ("")           
            sys.exit (0) 

    #mapper
    #used to pik out requires values from keys
    def dict_entry_from_db(self, value, key = 'username'):
        """
        keys = ['group', 'title', 'username']
        value is the data you store ino the db, that corresponds with
        the key above ..
        e.g.
        auth   = authpack()
        result = auth.dict_entry_from_db('hdaannaa@gmail.com','username')
        
        hence, the bottum line is , to take fetch the whole document from the db
        into your script or app, this function helps you to select ceratain unique
        keys from which their input values are known,
        NOTE: one cannot fetch passwords
        """
    
        try:
            db = self.get_base()
            for e in db.entries:
            
                title = str(e.title)
                username = str(e.username)
                password = str(e.password)
                url = str(e.url)
                group =  str(re.findall(r'title=\b\w+\b', str(e.group))[0].split('=')[1])
                
                new_keys_to_values, old_keys_to_new_keys, old_keys_to_values = self.mapperx (username, password, group, title, url)
                maps = new_keys_to_values
              
                if maps[key] == value and key != 'password':
                    self.log ("[+] Query: {} was successful".format(value))
                    return maps                    
        except Exception as err:
            self.log ("[+] [Reading function]")
            self.log ("[+] Could not fetch the specific query form the db")
            self.log (err)
            self.log ("")           
            sys.exit(0) 
                        
            
    def view_entries_from_db(self): 
        try:
            count = 0            
            print ("")
            print ("")
           
            # this is to index the mapper and fetch the custom field mappings
            q,w,e, = self.mapperx ();dm={v:k for k,v in w.iteritems()}
            #all_data = [["index", dm["group"], dm["username"]]]
            all_data=[]            
           
            db = self.get_base()          
            for n in db.entries:
                count = count + 1
                group =  str(re.findall(r'title=\b\w+\b', str(n.group))[0].split('=')[1])                
                data  = [str(count), group, n.username]
                all_data.append(data)
            
            #self.tabla(all_data)
            self.tabla(["index", dm["group"], dm["username"]], all_data)
            print ("")
            print ("")
            
        except Exception as err:
            self.log ("[+] [Viewing function]")
            self.log ("[+] Could not fetch the specific query form the db")
            self.log (err)
            self.log ("")           
            sys.exit(0)

    #mapper
    def dict_all_entries_from_db(self):

        try:
            db = self.get_base()
            l=[]
            for e in db.entries:
            
                title = str(e.title)
                username = str(e.username)
                password = str(e.password)
                url = str(e.url)
                group =  str(re.findall(r'title=\b\w+\b', str(e.group))[0].split('=')[1])
                
                new_keys_to_values, old_keys_to_new_keys, old_keys_to_values = self.mapperx (username, password, group, title, url)
                maps = new_keys_to_values
                
                l.append(maps)
            return l                
        except Exception as err:
            self.log ("[+] [Listing function]")
            self.log ("[+] Could not fetch the specific query form the db")
            self.log (err)
            self.log ("")           
            sys.exit(0)


    def handler(self, signum, frame):
        print ("")
        print ("")
        print ("[] Since you pressed CTRL+C ")
        print ("[] This program will terminate gracefully ...")
        print ("[] ----")
        print ("[] Copyright (c) 2020, Hud Seidu Daannaa ...")
        print ("[] www.daannaa.space")
        print ("")
        sys.exit(1989)


    def input_ (self):

        try:
        
            print ("")
            print ("")

            # Copyright (c) 2020, Hud Seidu Daannaa
            # All rights reserved.

            signal.signal(signal.SIGINT, self.handler)
            while True:
            
                print ("{}".format(self.banner))
                print ("    Specify an option:")
                print ("")
                print ("")
                #print ("  i\I = Register a Database [Db]")
                print ("    0 = Data view")
                print ("    1 = Data input")
                print ("    2 = Data deletion")
                print ("  c/C = Clear screen")
                print ("  q/Q = Exit [or hit <CTRL+C>]")
                print ("")
                print ("")
                optt = str(raw_input('Controlpanel@hud:/# '))
                
              
                
                if optt == '0':
                    try:
                        self.view_entries_from_db()
                        print ("")
                        print ("")
                        carry_on_after_view = raw_input("Press the Enter key to continue ...")
                        
                    except Exception as er:
                        self.log ("[+] [calling view]")
                        self.log (er)
                        print ("")
                        print ("App Interrupted")
                        print ("")
                        
                if optt.upper() == 'Q':
                    print ("")
                    print ("")
                    print ("")
                    print ("")
                    sys.exit(0)
                
                elif optt == '2':
                    try:
                        print ("")
                        print ("[+] Please input group to delete [REQUIRED] !!!")
                        print ("[+] To exit prompt ,hit <CTRL+C> ")
                        print ("")
                        groupxx = str(raw_input('    Enter: '))
                        self.delete_entries_in_db(groupxx)
                        time.sleep(1)
                        #sys.exit(0)
                        #continue
                        
                    except Exception as er:
                        self.log ("[+] [calling deletion]")
                        self.log (er)
                        print ("")
                        print ("App Interrupted")
                        print ("")
                 


                 
                elif optt == '1':
                   
                    while True:                    
                        try:
                            new_keys_to_values, old_keys_to_new_keys, old_keys_to_values = self.mapperx ()
                            o = old_keys_to_new_keys
                            
                            msg = {}
                            for k, v in o.iteritems():
                                
                                if v == 'group': 
                                    
                                    print ("")
                                    print ("[+] This field is mandatory [REQUIRED]")
                                    print ("[+] NOTE: {} should be a unigue parameter .... ".format(k))
                                    print ("[+]       hence if your goal is to use only [username/password] fields")
                                    print ("          just click [Enter] and proceed ....")
                                    print ("")
                                    
                                    group = str(raw_input('    Enter {} : '.format(k)))
                                    if len(group) == 0:
                                        group = str(self.generate_roup())                        
                                    msg[k] = group
                                
                                if v == 'username':
                                    print ("")
                                    print ("[+] This field is mandatory [REQUIRED]")
                                    username = str(raw_input('    Enter {} : '.format(k)))
                                    if len(username) == 0:
                                        username = 'na'
                                    msg[k] = username
                                    
                                if v == 'password':
                                    two=False
                                    try:
                                        password = self.get_pass(k)
                                        msg[k] = "Verified !"
                                    except:
                                        two=True
                                    # finally:
                                    # this is a lik to exit the password loop, back to the home page
                                    if two==True:
                                        break
                                    
                                if v == 'title':
                                    print ("")
                                    print ("[+] This is an field [OPTIONAL]")
                                    print ("    just hit [Enter] if not applicable..")
                                    print ("")
                                    title = str(raw_input('    Enter {} : '.format(k)))
                                    if len(title) == 0:
                                        title = 'na'
                                    msg[k] = title
                                    
                                if v == 'url':
                                    print ("")
                                    print ("[+] This is an field [OPTIONAL]")
                                    print ("    just hit [Enter] if not applicable..")
                                    print ("")
                                    url = str(raw_input('    Enter {} : '.format(k)))
                                    if len(url) == 0:
                                        url = 'na'
                                    msg[k] = url                                    
                                            
                        except Exception as er:
                            self.log ("[+] taking inputs")
                            self.log (er)
                            pass
                        
                        # this is a lik to exit the password loop, back to the home page
                        if two==True:
                            break
                                                
                        print ("")
                        print ("")
                        print ("")
                        print ("[+] Please confirm if the following inputs are correct")
                        print ("")

                        for k, v in msg.iteritems():
                            print ("    {0}: {1}".format(k, v))
                        print ("")

                        # confirmation
                        # raw_input("Press Enter to continue...")
                        ten      = False
                        validate = raw_input("[+] Enter Y/y[Yes] to confirm N/n[No] : ")
                        while True:
                        
                            if validate.upper() == 'Y':
                                print ("")
                                print ("[+] Confirmation is affirmative")
                                print ("[+] Application will procceed")
                                #time.sleep(2)
                                try:
                                    ddb      =  authpack()
                                    res      =  self.write_entries_to_db(username, password, group, title, url)
                                    print ("[+] Credentials were written ..")
                                except Exception as er:
                                    self.log ("[+] calling writer")
                                    print ("[+] Credentials were not written ..")
                                    self.log (er)
                                
                                print ("[+] ========================")
                                print ("[+] The system will now exit gracefully ...")
                                print ("")
                                time.sleep(1)
                                #sys.exit(0)
                                ten = True
                                
                                # this is a lik to exit the validation loop, back to the home page
                                if ten == True:
                                    break
                                                                                                                               
                            elif validate.upper() == 'N':
                                time.sleep(2)
                                print ("")
                                print ("[+] The app will reboot:")
                                print ("")
                                break
                            else:
                                print ("")
                                print ("[+] INVALID input")
                                print ("[+] Please read instructions, and enter a valid input")
                                print ("[+] Enter Y/y[Yes] to confirm N/n[No] : ")
                                print ("")
                                validate = raw_input("Enter Y/y[Yes] to confirm N/n[No] : ")
                        
                        # this is a lik to exit the validation loop, back to the home page
                        if ten == True:
                            break
                        # this is a lik to exit the password loop, back to the home page
                        if two==True:
                            break
                            
                


                elif optt.upper() == 'C':
		    if platform.system()=='Windows':os.system('cls')
                    elif platform.system()=='Linux':os.system('clear')
		    else:
			print ("")
			print ("[+] Command not applicable ..")
			print ("")
                            
                            
                else:
                    #print ("")
                    print ("")
                    #print ("[+] INVALID input")
                    print ("")
                    continue
        except Exception as er:
            #self.log ("[+] taking inputs")
            self.log (er)
            print ("")
            print ("App Interrupted")
            print ("")
