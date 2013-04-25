#!/usr/bin/python
import cgi

def buildUserDictionary(inputFile):
    userDictionary = {}
    users = inputFile.readlines()
    for user in users:
        values = user.rstrip().split(";")
        userDictionary[values[0]] = values[1]
    return userDictionary

if __name__ == '__main__':
    result =''
    inputs = cgi.FieldStorage()
    loginType = inputs.getvalue("loginType")
    username = inputs.getvalue("username")
    password= inputs.getvalue("password")
#    loginType = raw_input("loginType")
#    username = raw_input("username")
#    password = raw_input("password")
    
    
    
    with open("userDatabase.txt", "a+") as database:
        userDictionary = buildUserDictionary(database)
        global result
        if loginType == "0":
            if username in userDictionary and userDictionary[username]==password:
                result = "You have successfully logged in!"
            else:
                result = "Error: incorrect username/password combination. Please try again."
        if loginType == "1":
            if username in userDictionary:
                result = "Error: the username '%s' has already been taken." %(username)
            else:
                database.write("\n" + username + ";" + password)
                result = "Account '%s' has been successfully created" %(username)
    

    print "Content-Type: text/html"
    print
    print result
        