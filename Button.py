import pygame

class Button:
    def __init__(self, x, y, width, height, text, action, font_size=24, font_color=(255, 255, 0), bg_color=(50, 50, 50)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, font_size)
        self.text_surface = self.font.render(self.text, True, font_color)
        self.bg_color = bg_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.text_surface, (self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2, self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2))