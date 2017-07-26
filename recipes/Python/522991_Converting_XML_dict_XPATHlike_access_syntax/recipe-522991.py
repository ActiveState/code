import sys
from cStringIO import StringIO
from xml.parsers import expat

def list_to_xml(name, l, stream):
   for d in l:
      dict_to_xml(d, name, stream)

def dict_to_xml(d, root_node_name, stream):
   """ Transform a dict into a XML, writing to a stream """
   stream.write('\n<' + root_node_name)
   attributes = StringIO() 
   nodes = StringIO()
   for item in d.items():
      key, value = item
      if isinstance(value, dict):
         dict_to_xml(value, key, nodes)
      elif isinstance(value, list):
         list_to_xml(key, value, nodes)
      elif isinstance(value, str) or isinstance(value, unicode):
         attributes.write('\n  %s="%s" ' % (key, value))
      else:
         raise TypeError('sorry, we support only dicts, lists and strings')

   stream.write(attributes.getvalue())
   nodes_str = nodes.getvalue()
   if len(nodes_str) == 0:
      stream.write('/>')
   else:
      stream.write('>')
      stream.write(nodes_str)
      stream.write('\n</%s>' % root_node_name)

def dict_from_xml(xml):
   """ Load a dict from a XML string """

   def list_to_dict(l, ignore_root = True):
      """ Convert our internal format list to a dict. We need this
          because we use a list as a intermediate format during xml load """
      root_dict = {}
      inside_dict = {}
      # index 0: node name
      # index 1: attributes list
      # index 2: children node list
      root_dict[l[0]] = inside_dict
      inside_dict.update(l[1])
      # if it's a node containing lot's of nodes with same name,
      # like <list><item/><item/><item/><item/><item/></list>
      for x in l[2]:
         d = list_to_dict(x, False)
         for k, v in d.iteritems():
            if not inside_dict.has_key(k):
               inside_dict[k] = []
               
            inside_dict[k].append(v)

      ret = root_dict.values()[0] if ignore_root else root_dict
         
      return ret
   
   class M:
      """ This is our expat event sink """
      def __init__(self):
         self.lists_stack = []
         self.current_list = None
      def start_element(self, name, attrs):
         l = []
         # root node?
         if self.current_list is None:
            self.current_list = [name, attrs, l]
         else:
            self.current_list.append([name, attrs, l])

         self.lists_stack.append(self.current_list)
         self.current_list = l         
         pass
          
      def end_element(self, name):
         self.current_list = self.lists_stack.pop()
      def char_data(self, data):
         # We don't write char_data to file (beyond \n and spaces).
         # What to do? Raise?
         pass

   p = expat.ParserCreate()
   m = M()

   p.StartElementHandler = m.start_element
   p.EndElementHandler = m.end_element
   p.CharacterDataHandler = m.char_data

   p.Parse(xml)

   d = list_to_dict(m.current_list)
   
   return d

class ConfigHolder:
    def __init__(self, d=None):
        """
        Init from dict d
        """
        self.d = {} if d is None else d

    def __str__(self):
        return self.d.__str__()

    __repr__ = __str__

    def load_from_xml(self, xml):
        self.d = dict_from_xml(xml)

    def load_from_dict(self, d):
        self.d = d

    def get_must_exist(self, key):
        v = self.get(key)

        if v is None:
            raise KeyError('the required config key "%s" was not found' % key)

        return v

    def __getitem__(self, key):
        """
        Support for config['path/key'] syntax
        """
        return self.get_must_exist(key)

    def get(self, key, default=None):
        """
        Get from config using a filesystem-like syntax

        value = 'start/sub/key' will
        return config_map['start']['sub']['key']
        """
        try:
            d = self.d

            path = key.split('/')
            # handle 'key/subkey[2]/value/'
            if path[-1] == '' :
                path = path[:-1]
            
            for x in path[:len(path)-1]:
                i = x.find('[')
                if i:
                   if x[-1] != ']':
                      raise Exception('invalid syntax')
                   index = int(x[i+1:-1])
                   
                   d = d[x[:i]][index]
                else:
                   d = d[x]

            return d[path[-1]]

        except:
            return default



def DoTest():
    config_dict = \
    { \
      'config_name': 'test',
      'source':
          {
           'address': 'address_value',
           'port': 'port_value',
          },
      'destination':
          {
           'address': 'address_value',
           'port': 'port_value',
           'routing_exceptions':
               {
                'test':
                    {
                     'address': 'localhost',
                     'port': 'port_value'
                    }
               }
          },
      'lists' :
      {
         'list_item':
            [
               { 'address' : 'address_value',
                 'port' : 'port-value'
               },
               { 'address' : 'address_value',
                 'port' : 'port-value'
               }
            ]
      }
    }


    test_count = 3
    previous_xml = None

    for x in range(test_count):
       s = StringIO()
       dict_to_xml(config_dict, 'config', s)

       xml = s.getvalue()
       print xml

       config_dict = dict_from_xml(xml)
       print config_dict

       if previous_xml != None:
          assert xml == previous_xml

       previous_xml = xml

       # using XPATH like syntax
       print config_dict['destination'][0]['port']
       print config_dict['destination'][0]['routing_exceptions'][0]['test'][0]['address']
       print config_dict['lists'][0]['list_item'][1]['address']

       # ConfigHolder makes it even easier       
       t = ConfigHolder()
       t.load_from_dict(config_dict)

       print t['destination[0]/port']
       print t['lists[0]/list_item[1]/address']


if __name__ == '__main__':
    DoTest()
