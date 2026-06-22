import tmxlib

# def to_obj(map : pygame.surface ,tiles : dict):
#         print('test')

#         #directions = dict(left = False,right = False, top = False, down = False)

#         for x in range(map.statics.get_width()):
#             for y in range(map.statics.get_height()):
#                 directions = dict(left = False,right = False, top = False, down = False)

#                 data = map.statics.get_at((x,y))
                

#                 if x > 0:
#                     if map.statics.get_at((x-1,y)) == (255,255,255,255):
#                         #there is a block to the left
#                         directions['left'] = True
                        
#                 if x < map.statics.get_width()-1:
#                     if map.statics.get_at((x+1,y)) == (255,255,255,255):
#                         #there is a block to the right
#                         directions['right'] = True
#                 if y > 0:
#                     if map.statics.get_at((x,y-1)) == (255,255,255,255):
#                         #there is a block below
#                         directions['down'] = True
                
#                 if y < map.statics.get_height()-1:
#                     if map.statics.get_at((x,y+1)) == (255,255,255,255):
#                         #there is a block above
#                         directions["top"] = True

#                 if data == (255,255,255,255):
#                     floor = Object(body_type=Body.STATIC)
#                     floor.body.position = x*32,y*32
#                     floor.add_shape(pymunk.Poly(floor.body,[(0,0),(32,0),(32,32),(0,32)],radius=1),10,2)
                       
#                     if directions["down"] and directions["top"]:
#                         #block below and above us
#                         if directions['right'] and not directions["left"]:
#                             #there is a block to the right
#                             floor.add_from_tileset(tiles['4'])
#                         elif directions['left'] and not directions["right"]:
#                             floor.add_from_tileset(tiles['6'])
                    
#                     elif directions["top"]:
#                         #block above us
#                         if directions["left"] and not directions['right']:
#                             #and a block to the left
#                             floor.add_from_tileset(tiles['3'])
#                         elif directions["right"] and not directions['left']:
#                             floor.add_from_tileset(tiles['1'])
#                         elif directions["left"] and directions["right"]:
#                             floor.add_from_tileset(tiles['2'])
#                     elif directions["down"]:
#                         #block above us
#                         if directions["left"] and not directions['right']:
#                             #and a block to the left
#                             floor.add_from_tileset(tiles['9'])
#                         elif directions["right"] and not directions['left']:
#                             floor.add_from_tileset(tiles['7'])
#                         elif directions["left"] and directions["right"]:
#                             floor.add_from_tileset(tiles['8'])
                            
        
#                     elif directions["right"] and directions["left"] and not directions["top"] and not directions["down"]:
#                         floor.add_from_tileset(tiles['2'])

#                     else:
#                         floor.add_from_tileset(tiles['5'])



#                     sprite_group.add(floor)
#                     floor.shape.friction = 0.5
                                          
                

#                 if data == (255,00,00,255):
#                     obj = Object(body_type=Body.DYNAMIC)
#                     obj.body.position = x*32,y*32
#                     obj.add_shape(pymunk.Poly(obj.body,[(0,0),(30,0),(30,30),(0,30)]),5,2)
#                     obj.add_image("Textures/doos.png")
#                     sprite_group.add(obj)
#                     obj.shape.friction = 0.3

