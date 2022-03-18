class locations:
     '''type = classroom
              noEnter
              corridor
              big
              stairs

        scroll = x
                 y'''
     def __init__(self , type , scroll = False):
          self.type = type
         
class classroom(locations):
    def hitbox():
        pass

class noEnter(locations):
    def noEnterMsg(msg):
        #msg = pyg.draw.rect(
        pass

class corridor(locations):
    def cor_scroll(dir):
        '''dir = x
                 y'''
        pass

class big(locations):
    def big_scroll():
        pass

class stairs(locations):
    def stair():
        pass


gOffice = noEnter
