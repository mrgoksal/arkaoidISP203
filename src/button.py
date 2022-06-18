from configs import *
from src.text_object import TextObject

# Класс описания кнопок
class Button:
    # Инициализация
    def __init__(self, x, y, message, width=BUTTON_W, height=BUTTON_H, color=(110, 110, 110), font_size=50):
        self.text_object = TextObject(x, y, message, color, font_size)
        self.width = width
        self.height = height
        self.inactive_clr = (57, 50, 50) # Неактивный цвет
        self.active_clr = (13, 162, 58) # Активный цвет
        self.is_pressed = False

    # Метод отрисовки + создание кликабельной области
    def draw(self, sc, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Проверка вхождения положения мыши в положение кликабельной области
        if self.text_object.pos[0] < mouse[0] < self.text_object.pos[0] + self.width \
                and self.text_object.pos[1] < mouse[1] < self.text_object.pos[1] + self.height:
            self.text_object.color = self.active_clr
            # Отслеживание нажатия левой кнопки мыши
            if click[0] == 1:
                pygame.time.delay(300)

                if action is not None:
                    action()
                self.is_pressed = True

        else:
            self.text_object.color = self.inactive_clr
            self.is_pressed = False

        self.text_object.draw(sc)

        return self.is_pressed
