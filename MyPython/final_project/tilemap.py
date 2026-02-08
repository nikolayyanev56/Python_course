from tiles import StaticTile
import os
import pygame
Surface = pygame.surface.Surface
Rect = pygame.rect.Rect
ImageLoad = pygame.image.load
Path = os.path


class TileMapLayer():
    def __init__(self, tile_data: dict, map_rect: Rect, tile_atlas):
        self.rect = map_rect
        self.surf = Surface((self.rect.x, self.rect.y))
        self.tile_data = tile_data
        self.atlas = ImageLoad(tile_atlas)
    

    def build_map(self):
        self.tile_data
        for tile in self.tile_data:
            pass


    def get_tile(atlas, x: int, y: int):
        return Surface()


def build_static_layer(tile_data: dict, tile_size: int ,layer_rect: Rect, atlas_path: Path):
    """
    Used for drawing the static tiles once on a single surface,\n
    tile_data is a dict containing lists of grid and atlas coords\n
    for the tiles
    """
    atlas = ImageLoad(atlas_path).convert_alpha()
    static_layer = Surface((layer_rect.x * tile_size, layer_rect.y * tile_size))
    physics_layer = []

    for tile_id, coords in tile_data.items():
        #unpack coords
        grid_pos, atlas_pos = coords

        #get the texture
        src_x = atlas_pos[0] * tile_size
        src_y = atlas_pos[1] * tile_size
        src_rect = Rect(src_x, src_y, tile_size, tile_size)

        #put it on the surface
        grid_x = grid_pos[0] * tile_size
        grid_y = grid_pos[1] * tile_size
        static_layer.blit(atlas, (grid_x, grid_y), src_rect)
        tile_rect = Rect(grid_x, grid_y, tile_size, tile_size)
        physics_layer.append(tile_rect)
    
    return static_layer, physics_layer