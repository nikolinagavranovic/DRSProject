from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot


class Worker(QObject):

    finished = pyqtSignal()
    update = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.thread = QThread()
        # move the Worker object to the Thread object
        # "push" self from the current thread to this thread
        self.moveToThread(self.thread)
        # Connect Worker Signals to the Thread slots
        self.finished.connect(self.thread.quit)
        # Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.work)

    def start(self):
        # Start the thread
        self.thread.start()

    @pyqtSlot()
    def work(self):  # A slot with no params
        pass
