from init import *

util.clear()

imgs = Lib_imgs("./imgs").get()

winSize = (imgs["bg_hushhouse.png"].get_rect()[2:])
Window = Window(winSize, imgs["bg_hushhouse.png"])

Book = Item(imgs["bookCover.png"], 0.1, (100, 100))

fps = 60

running = True
while running:
    pygame.time.Clock().tick(fps)
    
    Window.renderingQueue(Book.get())

    Window.update(*Window.draw(Window.getQueue()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            Book.dragging(True)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            Book.dragging(False)
        if pygame.mouse.get_pressed()[0]:
            Book.drag()
Window.quit()
