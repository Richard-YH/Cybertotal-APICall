from api_table import RESTful_API
import re
import requests
import string, random, json



my_token = 'Token'
cybertotal = f"https://cybertotal.cycarrier.com"

#判斷IOCs 種類
def IOC_type(IOC):
  try:
    matching_dict = lambda x: {
      bool(re.fullmatch("(\d+\.+\d+\.+\d+\.+\d+\Z)",x)) == True: 'ip',
      bool(re.fullmatch("^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",x)) == True: 'email',
      bool(re.fullmatch("^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$",x)) == True: 'domain',
      bool(re.fullmatch("^(((([a-z,1-9]+)|[0-9,A-Z]+))([^a-z\.]))*",x)) == True: 'hash', 
      bool(re.fullmatch("((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)",x)) == True: 'url', #ip會不行
    }
    return matching_dict(IOC)[True]
  except:
    pass
def diction_name():
    length_of_string = 8
    randomName = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))+'.json'
    return randomName
  
def api_call(ioc,parameter):
  #Part 1 Manage hard disk search
  #search Filepath Table and get filepath
  try:
    with open('Database/filepath_table', 'r') as f:
        filepath_table = json.load(f)
        dict_name = filepath_table[ioc+" -"+parameter]
        print(f"[*] {dict_name} filepath found !")
    with open("Database/"+dict_name, 'r') as f:
        ioc_info = json.load(f)
        print(f"[*] {dict_name} exist !")
    return ioc_info

  except:
    print("[*] File not found on local ")
    #part2 cybertotal api call
    restful_api=cybertotal+RESTful_API(IOC_type(ioc),parameter)+ioc
    try:
      r = requests.get(restful_api, headers={'Authorization': my_token} ) #RESTful API

      if r.status_code == 404:
        return f"[*] '{ioc}' Indiactor not found"

      elif r.status_code == 200: #not test
        ioc_info = r.json()
        #add new dict to Filepath Table
        dict_name = diction_name()
        dic = { ioc+" -"+parameter :  dict_name }
        with open('Database/filepath_table', 'r+') as f:
          filepath_table = json.load(f)
        filepath_table.update(dic)
        with open('Database/filepath_table', 'r+') as f:
          json.dump(filepath_table, f)
          print("[*] Successfully written file path to file path table")
        #save result to Json Result

        with open("Database/"+dict_name, 'w+') as f:
          json.dump(ioc_info, f)
          print(f"[*] {dict_name} saved successfully\n")
        return ioc_info

      else:
        print(f"[*] {r.status_code} error")
        return "[*] Status error with your request\n"
    except:
      #print("api call function error")
      return "[*] api call function error\n"
      pass

if __name__=='__main__':

  while True:
    print("Please enter IOC and parameter：")
    try:
      input_string = input('')
      if input_string == "exit":
        break
      else:
        ioc,parameter = input_string.split(' -')
        ioc_info = api_call(ioc,parameter)
        print(f'{ioc_info}\n')

    except:
      print("[*] Input error, please enter the correct format : ioc [-paramater]\n")
      pass







