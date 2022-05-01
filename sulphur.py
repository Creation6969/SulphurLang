from sys import *
import time
import platform
import os

name = ""
tokens = []

file = open(argv[1], "r").read()

def lex(content):
  content = list(content)
  tok = ""
  tex = ""
  state = 0
  for char in content:
    tok += char
    if tok == " ":
      if state == 0:
        tok = ""
      else: 
        tok=" "
    elif tok == "\n":
        tok = ""
    elif tok == "::":
      tokens.append("sp")
      tok = ""
    elif tok == "assert": 
      tokens.append("assert")
      tok = ""
    elif tok == "false":
      tokens.append("false")
      tok = ""
    elif tok == "true":
      tokens.append("true")
      tok = ""
    elif tok == "getShellArg":
      tokens.append("getShellArg")
      tok=""
    elif tok == "renameFile":
      tokens.append("renameFile")
      tok = ""
    elif tok == "deleteFile": 
      tokens.append("deleteFile")
      tok = ""
    elif tok == "exitProgram":
      tokens.append("exitProgram")
      tok = ""
    elif tok == "shellExecute":
      tokens.append("shellExecute")
      tok = ""
    elif tok == "writeToFile":
      tokens.append("writeToFile")
      tok = ""
    elif tok == "readFile":
      tokens.append("readFile")
      tok = ""
    elif tok == "logLine":
      tokens.append("logLine")
      tok = ""
    elif tok == "wait":
      tokens.append("wait")
      tok = ""
    elif tok == "\"":
      if state == 0:
        state = 1
      elif state == 1:
        tokens.append("str:" + tex + "\"")
        tex = ""
        state = 0
        tok = ""
    elif state == 1:
      tex += tok
      tok = ""
      
  return tokens
  # print(tokens)


def parse(toks):
  i = 0
  while (i < len(toks)):
    if toks[i] == "exitProgram":
      exit()
      i+=1
    elif toks[i] == "logLine":
      if toks[i+1][0:3] == "str":
        print(toks[i+1][4:].replace("\"", ""))
        i+=2
      elif toks[i+1]+" "+toks[i+2][0:3] == "readFile str":
        print(open(toks[i+2][4:].replace("\"", ""), "r").read())
        i+=3
    elif toks[i]+" "+toks[i+1][0:3] =="wait str":
      time.sleep(float(toks[i+1][4:].replace("\"", "")))
      i+=2
    elif toks[i]+" "+toks[i+1][0:3] == "shellExecute str": 
      os.system(toks[i+1][4:].replace("\"",""))
      i+=2
    elif toks[i]+" "+toks[i+1][0:3]+" "+toks[i+2][0:3] == "renameFile str str":
      a = toks[i+1][4:].replace("\"", "")
      b = toks[i+2][4:].replace("\"", "")
      os.rename(a, b)
      i+=3
    elif toks[i] == "assert":
      if toks[i+1]+" "+toks[i+2]+" "+toks[i+3][0:3] == "true sp str":
        pass
      elif toks[i+1]+" "+toks[i+2]+" "+toks[i+3][0:3] == "false sp str":
        bean = toks[i+3][4:].replace("\"", "")
        print(f"AssertionError: {bean}")
        exit()
      i+=4
    elif toks[i]+" "+toks[i+1][0:3]+" "+toks[i+2] == "writeToFile str sp":
      if toks[i+3][0:3] == "str":
        y = toks[i+1][4:].replace("\"", "")
        z = toks[i+3][4:].replace("\"", "")
        f = open(y, "w")
        f.write(z)
        f.close()
        i+=4
      elif toks[i+3]+" "+toks[i+4][0:3] == "getShellArg str":
        YB = toks[i+1][4:].replace("\"", "")
        VB = toks[i+4][4:].replace("\"", "")
        FB = open(YB, "w")
        FB.write(argv[int(VB)+1])
        FB.close()
        i+=5
        
def run():
  ntks = lex(file)
  parse(ntks)
  
run() 

