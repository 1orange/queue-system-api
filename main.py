import tkinter

from assets.classes.Client import Client
from assets.classes.Queue import Queue

def init_canvas():
    root = tkinter.Tk()
    root.title('intersection')
    canvas = tkinter.Canvas(root, width = '800', height = '800', bg = 'white')
    canvas.pack(side='right')

    return root, canvas

def canvas_create_buttons(root, queue):
    doButton = tkinter.Button(root, text = 'add car', command = lambda:add())
    doButton.pack()

    removeButton = tkinter.Button(root, text = 'remove car', command = lambda:remove())
    removeButton.pack()

    but = tkinter.Button(root, text = 'asd car', command = lambda:move())
    but.pack()


if __name__ == "__main__":
    # Init canvas
    #tk_root, canvas = init_canvas()

    clients = set()
    queue = Queue()

    for _ in range(15):
        current_client = Client()
        clients.add(current_client)

        queue.enqueue(current_client)

    #print(queue.get_size())
    queue.preview()
    #print(clients)


    # Insert buttons
    #canvas_create_buttons(tk_root, canvas, queue)

    #tk_root.mainloop()