# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$3-nov-2011 22.03.35$"

from configobj import ConfigObj
from validate  import Validator

class o_cfg :
    def __init__(self, config_file, config_spec=None):
        self.configspec = ConfigObj(config_spec, interpolation=False, list_values=True, _inspec=True)
        self.configfile = ConfigObj(config_file, configspec=self.configspec)
    
    def parse_config(self):
        vars = {}
        validator = Validator()
        result = self.configfile.validate(validator)
        for section in self.configfile :
            vars["%s" % (section)]=self.configfile[section]
            
        return vars
            
