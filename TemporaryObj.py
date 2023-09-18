from GameObject import GameObject
import time

class TemporaryObj(GameObject):
    def __init__(self, x, y, sprite, time_to_live):
        super().__init__(x, y, sprite)
        self.time_to_live = time_to_live
        self.last_update_time = time.time()

    def update(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        self.time_to_live -= elapsed_time
        self.last_update_time = current_time
        print(self.time_to_live)
        if self.time_to_live <= 0:
            print("DELETING SELF")
            self.delete_self()