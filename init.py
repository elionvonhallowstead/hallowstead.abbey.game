from os.path import isfile, join
from os import listdir
import pygame, util

def getMousePos() -> tuple[int, int]:
    return pygame.mouse.get_pos()
    

class Window:
    def __init__(self, winSize:tuple[int, int], backdrop:pygame.surface.Surface) -> None:
        pygame.init()

        self._winSize = winSize
        self._backdrop = backdrop

        self._win = pygame.display.set_mode(winSize, pygame.RESIZABLE)
        return None

    def updateWinSize(self) -> tuple[int, int]:
        self._winSize = self._win.get_size()
        return self._winSize

    def _setBackdrop(self, backdrop) -> tuple[pygame.surface.Surface, pygame.rect.Rect]:
        self._win.fill(pygame.color.THECOLORS["black"])
        backdrop = pygame.transform.scale(backdrop, self._winSize)
        return (backdrop, backdrop.get_rect())

    def get(self) -> pygame.surface.Surface:
        return self._win

    def renderingQueue(self, *elements:tuple[pygame.surface.Surface, pygame.rect.Rect]) -> None:
        self._queue = [self._setBackdrop(self._backdrop)]
        for element in elements:
            self._queue.append(element)
        return None

    def getQueue(self) -> tuple[tuple[pygame.surface.Surface, pygame.rect.Rect]]:
        return self._queue

    def draw(self, queue:list[tuple[pygame.surface.Surface, pygame.rect.Rect]]) -> list[pygame.rect.Rect]:
        tmp = queue.copy()
        for i in tmp:
            queue = [i for i in queue if self._win.get_rect().colliderect(i[1])]
        if not util.isEmpty(queue):
            return self._win.blits(queue)
        return []

    def update(self, *queue:pygame.rect.Rect) -> list:
        self._winSize = tuple(self._win.get_rect()[2:])
        queue = list(queue)
        if not util.isEmpty(queue):
            pygame.display.update(queue)
        return queue
    
    def quit(self) -> None:
        pygame.quit()
        return None

class Lib_imgs:
    def __init__(self, pathToFolder:str) -> None:
        self._imgs = {}
        files = []
        for file in listdir(pathToFolder):
            if isfile(join(pathToFolder, file)):
                files.append((pygame.image.load, join(pathToFolder, file)))
        files = util.multiThread(4, *files, prefix="load.")
        self._imgs = {i[0].split('/')[-1]: files.get(i) for i in files}
        return None

    def get(self) -> dict:
        return self._imgs

class Item:
    def __init__(self, sprite:pygame.surface.Surface, winSize:tuple[int, int], scale:float=1, pos:tuple[int, int]=(0, 0)) -> None:
        self._originalSprite = sprite
        self._scale = scale
        self._baseSprite = pygame.transform.scale_by(self._originalSprite, scale)
        self._dragSprite = pygame.transform.scale_by(self._originalSprite, scale+0.01)
        self._sprite = self._baseSprite
        self._rect = self._sprite.get_rect()
        self._size = self._rect.size
        self._rect.topleft = pos
        self._relativeSize = (pos[0]/winSize[0], pos[1]/winSize[1])
        self._getsDragged = False
        self._dragOffset = (0, 0)

        self._originalWinSize = winSize
        self._winSize = winSize
        return None

    def get(self) -> tuple[pygame.surface.Surface, pygame.rect.Rect]:
        return (self._sprite, self._rect)

    def updateCoords(self, winSize:tuple[int, int]) -> tuple[int, int]:
        self._winSize = winSize
        self._baseSprite = pygame.transform.scale_by(self._originalSprite, self._scale * self._winSize[0] / self._originalWinSize[0])
        self._dragSprite = pygame.transform.scale_by(self._originalSprite, (self._scale+0.01) * self._winSize[0] / self._originalWinSize[0])
        self._sprite = self._dragSprite if self._getsDragged else self._baseSprite
        self._rect.topleft = (self._winSize[0]*self._relativeSize[0], self._winSize[1]*self._relativeSize[1])
        return self._rect.topleft

    def dragging(self, true:bool) -> None:
        if true:
            self._sprite = self._dragSprite
            if self._rect.collidepoint(pygame.mouse.get_pos()):
                mousePos = getMousePos()
                self._dragOffset = (self._rect.x - mousePos[0], self._rect.y - mousePos[1])
                self._getsDragged = True
        else:
            self._sprite = self._baseSprite
            if self._getsDragged:
                self._rect.topleft = (int(self._rect.centerx/self._size[0])*self._size[0], int(self._rect.centery/self._size[1])*self._size[1])
                self._relativeSize = (self._rect.topleft[0]/self._winSize[0], self._rect.topleft[1]/self._winSize[1])
            self._getsDragged = False
        return None

    def drag(self) -> pygame.rect.Rect:
        if self._getsDragged:
            mousePos = getMousePos()
            self._rect.topleft = (mousePos[0]+self._dragOffset[0], mousePos[1]+self._dragOffset[1])
        return self._rect
