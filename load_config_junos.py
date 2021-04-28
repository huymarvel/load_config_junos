import jinja2
import yaml
from datetime import date
import napalm
import os.path, shutil

now = date.today()
device={
        "username":"tdhuy",
        "password":"muahoado1C",
        "optional_args": {"port":22}
        }
#Delete old directory
path1 = "D:/Temp_py"
shutil.rmtree(path1, ignore_errors=True)
# Create folder Temp_py at disk D
if not os.path.exists(path1):
    os.makedirs(path1)
conf_file_name = f"D:/Temp_py/Config_{now.day}{now.month}{now.year}.txt"

#prepare conf file function
def create_data(template_j2,data_junos):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("."), lstrip_blocks=True, trim_blocks=True)
    template = env.get_template(template_j2)

    f = open(data_junos)
    data_tem_str = f.read()
    f.close()

    data_tem_dict = yaml.safe_load(data_tem_str)
    #print (data_tem_dict)
    configs = template.render(int = data_tem_dict)
    outFile=open(conf_file_name, "w")
    outFile.write(configs)
    outFile.close()
	
#delete interface config
def conf_delete_interface(ip_list_file):
    f = open(ip_list_file,"r")
    data_host = f.read()
    data_host = data_host.strip()
    data_host_lst = data_host.split(",")
    f.close()
    #print (data_host_lst)

    for IP_lo0 in data_host_lst:
        device["hostname"] = IP_lo0
        #print (device)
        driver = napalm.get_network_driver("junos")
        try:
            print("Connecting to {}...".format(device["hostname"]))
            conn = driver(**device)
            conn.open()
        except:
            print("Check IP, username, password, port")
        else:
            print ("Connected successful")
            
            print("Loading configuration...")
            conn.load_merge_candidate(filename = conf_file_name)
            print("Done")
            
            print()
            print("Comparing configuration...")
            diff = conn.compare_config()
            print(diff)
            
            print()
            choice = input("Do you want to commit?(y/n) ")
            if choice == "y":
                print("Committing...")
                conn.commit_config()
                print("Done!")
            else:
                print("Configuration is ignored")
                conn.discard_config()

            conn.close()
			
# load configuration
def conf_load (ip_list_file):
    f = open(ip_list_file,"r")
    data_host = f.read()
    data_host = data_host.strip()
    data_host_lst = data_host.split(",")
    f.close()
    #print (data_host_lst)

    for IP_lo0 in data_host_lst:
        device["hostname"] = IP_lo0
        driver = napalm.get_network_driver("junos")
        try:
            print("Connecting to {}...".format(device["hostname"]))
            conn = driver(**device)
            conn.open()
        except:
            print("Check IP, username, password, port")
        else:
            print("Connected successful")
            print("Loading configuration...")
            conn.load_merge_candidate(filename = conf_file_name)
            print("Done")

            print()
            print("Comparing configuration...")
            diff = conn.compare_config()
            print(diff)

            conn.commit_config()
            print("Done")
            conn.close()
create_data("template_conf.j2","data_conf.yml")
conf_load ("ip_list_test.txt")
			
#create_data("template_delete_int.j2","data_conf.yml")
#conf_delete_interface("ip_list_test.txt")

