import abc

class EXIF_base(object):

    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def evaluate(self):
        return

    @abc.abstractmethod
    def instantiate_rule(self, input) :
        
        return

    

    
    
