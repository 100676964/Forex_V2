#!/usr/bin/env python
# coding: utf-8

# In[25]:


import base64
import sys

def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string

def decode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


# stri='0123@helloworld'
# key="password123456789abcdefghijklmnopqrstuvwxyz"

# enstr=encode(key,stri)

# print(enstr)

# destr=decode(key, enstr)

# print(destr)


# In[ ]:




