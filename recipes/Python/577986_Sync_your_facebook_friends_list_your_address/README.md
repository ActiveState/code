## Sync your facebook friends list to your address book on Mac/iPhone/iPad  
Originally published: 2011-12-17 09:24:19  
Last updated: 2011-12-17 09:27:02  
Author: Shao-chuan Wang  
  
**READ BEFORE YOU USE THE CODE***

**Requirement**
1. Mac OS with python obj-c wrapper built-in. Typically, Mac OS Snow leopard, or Lion comes with python wrapper of objc.
2. If you want to also sync to your iphone, simply enable iCloud feature provided by apple, and run this script on a macbook with iCloud enabled.
3. Need fbconsole module, which can be downloaded at https://github.com/facebook/fbconsole


This script will download the profile pictures, first name, last name of your friends, and insert them into your address book if it does not exist.