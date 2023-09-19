from GameObject import GameObject
import time

class TemporaryObj(GameObject):
    def __init__(self, x, y, sprite, time_to_live, mark_for_removal_callback=None):
        super().__init__(x, y, sprite)
        self.time_to_live = time_to_live
        self.last_update_time = time.time()
        self.callback = mark_for_removal_callback

    def update(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        self.time_to_live -= elapsed_time
        self.last_update_time = current_time
        if self.time_to_live <= 0:
            self.mark_for_removal()

    def mark_for_removal(self):
        if self.callback:
            self.callback(self)