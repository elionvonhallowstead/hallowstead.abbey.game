from init import *

util.clear()

imgs = Lib_imgs("./imgs").get()
books = Lib_imgs("./imgs/books").get()

winSize = tuple(imgs["bg_hushhouse.png"].get_rect()[2:])
Window = Window(winSize, imgs["bg_hushhouse.png"])

books = {key: Item(books[key], winSize, scale=0.1, pos=(0, 0)) for key in books.keys()}

fps = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            winSize = Window.updateWinSize()
            for key in books.keys():
                books.get(key).updateCoords(winSize)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            for key in books.keys():
                books.get(key).dragging(True)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            for key in books.keys():
                books.get(key).dragging(False)

        if pygame.mouse.get_pressed()[0]:
            for key in books.keys():
                books.get(key).drag()

    Window.renderingQueue(*[books.get(key).get() for key in books.keys()])

    Window.update(*Window.draw(Window.getQueue()))

    pygame.time.Clock().tick(fps)
Window.quit()
