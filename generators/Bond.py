
import random
import json
from generators.Generator import Generator
from generators.NPC import  NPC
from jinja2 import Template
from jinja2.environment import Environment
from util import Filters


class Bond(Generator):
    """Generate a bond between two people 'you' and 'other'."""
    def __init__(self, redis, features={}):

        Generator.__init__(self,redis,features)

        # if self.you and self.other are not set, set them to defaults.
        if not hasattr(self,'you'):
            self.you='you' 

        # a random NPC
        if not hasattr(self,'other'):
            self.other=NPC(self.redis).name['full'] 

        # We put you and other in an array so we can randomly select
        # who is the subject and who is the object.
        members=[self.you,self.other]
        random.shuffle(members)
        if not hasattr(self,'either'):
            self.either=members[0] 
        random.shuffle(members)

        # We use partyA/partyB syntax in the templates
        if not hasattr(self,'partyA'):
            self.partyA=members.pop() 
        if not hasattr(self,'partyB'):
            self.partyB=members.pop() 

        # If we don't already have text, we need to render a template
        if not hasattr(self,'text'):
            #if we have it, we need to add a "when" as well
            if hasattr(self,'when'):
                self.template=self.when+', '+self.template
            self.text=self.render_template(self.template) 

        #final sentence is stored as self.text.
        # note the need for capitalization of the first character
        self.text=self.text[0].capitalize()+self.text[1:]
            

