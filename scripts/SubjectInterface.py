class SubjectInterface:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def deregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_remove_gameobject(self):
        for observer in self._observers:
            observer.mark_for_removal(self)


            