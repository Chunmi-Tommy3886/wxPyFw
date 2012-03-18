# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$3-nov-2011 22.03.35$"

from configobj import ConfigObj
from validate  import Validator

class o_cfg(ConfigObj):
    def __init__(self, config_file, config_spec=None):
        spec = None
        
        if config_spec is not None :
            spec = ConfigObj.__init__(self, config_spec, interpolation=False, list_values=True, _inspec=True)
            
        ConfigObj.__init__(self, config_file, configspec=spec)
    
    def parse_cfg(self):
        vars = {}
        validator = Validator()
        result = self.configfile.validate(validator)
        return result
            
