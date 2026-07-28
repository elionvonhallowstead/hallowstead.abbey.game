from os.path import isfile, join
from os import listdir
import pygame, util

class Window:
    def __init__(self, winSize:tuple[int, int], backdrop:pygame.surface.Surface) -> None:
        pygame.init()

        self._winSize = winSize
        self._backdrop = backdrop

        self._win = pygame.display.set_mode(winSize, pygame.RESIZABLE)
        return None

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
        self._winSize = self._win.get_rect()[2:]
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
    def __init__(self, sprite:pygame.surface.Surface, scale:float=1, pos:tuple[int, int]=(0, 0)) -> None:
        self._sprite = pygame.transform.scale_by(sprite, scale)
        self._rect = self._sprite.get_rect()
        self._pos = pos
        self._getsDragged = False
        self._dragOffset = (0, 0)

        self._rect.topleft = pos
        return None

    def get(self) -> tuple[pygame.surface.Surface, pygame.rect.Rect]:
        return (self._sprite, self._rect)

    def getPos(self) -> tuple[int, int]:
        self._pos = self._rect[2:]
        return self._pos

    def dragging(self, true:bool) -> None:
        mousePos = pygame.mouse.get_pos()
        if true:
            if self._rect.collidepoint(mousePos):
                self._getsDragged = True
                self._dragOffset = (self._rect.x - mousePos[0], self._rect.y - mousePos[1])
        else:
            self._getsDragged = False
        return None

    def drag(self):
        if self._getsDragged:
            mouse_pos = pygame.mouse.get_pos()
            self._rect.topleft = (mouse_pos[0] + self._dragOffset[0], mouse_pos[1] + self._dragOffset[1])
        return self._rect
