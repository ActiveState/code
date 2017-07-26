## autosetup for simplified default values 
Originally published: 2005-06-08 04:19:20 
Last updated: 2005-06-08 04:19:20 
Author: Taro Ogawa 
 
If each class's __init__ is used to set default values, it requires that one use super() or explicit parentclass.__init__() calls .  Such ugly boilerplate can be avoided with this recipe.