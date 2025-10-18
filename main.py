import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer, QRect, QUrl
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtMultimedia import QSoundEffect


class PingPong(QWidget):
    def __init__(self, ball_size):
        super().__init__()
        self.setWindowTitle("Пинг-Понг")
        self.setGeometry(100, 100, 600, 500)

        self.ball_size = int(ball_size)
        self.ball_x = 200
        self.ball_y = 150
        self.ball_dx = 3
        self.ball_dy = 3

        self.paddle_x = 150
        self.paddle_width = 100
        self.paddle_height = 10

        self.score = 0
        self.lives = 3
        self.game_over = False

        self.setMouseTracking(True)
        self.hit_sound = QSoundEffect()
        self.hit_sound.setSource(QUrl.fromLocalFile("kick.wav"))
        self.hit_sound.setVolume(0.5)  # громкость от 0.0 до 1.0

        # Кнопка перезапуска
        self.restart_button = QPushButton("Сыграть снова", self)
        self.restart_button.setGeometry(140, 130, 120, 40)
        self.restart_button.setVisible(False)
        self.restart_button.clicked.connect(self.restart_game)

        # Загрузка изображения
        self.background = QPixmap("unnamed.jpg")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Рисуем изображение справа
        if not self.background.isNull():
            scaled_bg = self.background.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = self.width() - scaled_bg.width() - 10
            y = (self.height() - scaled_bg.height()) // 2
            painter.drawPixmap(x, y, scaled_bg)

        # Мяч
        painter.setBrush(QColor("yellow"))
        painter.drawEllipse(int(self.ball_x), int(self.ball_y), self.ball_size, self.ball_size)

        # Ракетка
        painter.setBrush(QColor("blue"))
        painter.drawRect(int(self.paddle_x), self.height() - 20, self.paddle_width, self.paddle_height)

        # Текст: очки, жизни, скорость
        painter.setFont(QFont("Arial", 12))
        painter.setPen(QColor("black"))
        painter.drawText(10, 20, f"Очки: {self.score}")
        painter.drawText(10, 40, f"Жизни: {self.lives}")
        speed = math.sqrt(self.ball_dx**2 + self.ball_dy**2)
        painter.drawText(10, 60, f"Скорость: {speed:.2f}")

        # Надпись "Игра окончена"
        if self.game_over:
            painter.setFont(QFont("Arial", 24, QFont.Bold))
            painter.setPen(QColor("darkRed"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Игра окончена")

    def mouseMoveEvent(self, event):
        self.paddle_x = event.x() - self.paddle_width // 2
        self.paddle_x = max(0, min(self.paddle_x, self.width() - self.paddle_width))

    def update_game(self):
        if self.game_over:
            return

        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_x <= 0 or self.ball_x >= self.width() - self.ball_size:
            self.ball_dx *= -1
        if self.ball_y <= 0:
            self.ball_dy *= -1

        paddle_rect = QRect(int(self.paddle_x), self.height() - 20, self.paddle_width, self.paddle_height)
        ball_rect = QRect(int(self.ball_x), int(self.ball_y), self.ball_size, self.ball_size)

        if ball_rect.intersects(paddle_rect) and self.ball_dy > 0:
            self.ball_dy *= -1
            self.score += 1
            self.ball_dx *= 1.05
            self.ball_dy *= 1.05
            self.hit_sound.play()
            
        if self.ball_y > self.height():
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
                self.ball_dx = 0
                self.ball_dy = 0
                self.restart_button.setVisible(True)
            else:
                self.ball_x = 200
                self.ball_y = 150
                self.ball_dy = -abs(self.ball_dy)

        self.repaint()

    def restart_game(self):
        self.score = 0
        self.lives = 3
        self.ball_x = 200
        self.ball_y = 150
        self.ball_dx = 3
        self.ball_dy = 3
        self.game_over = False
        self.restart_button.setVisible(False)
        self.repaint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ball_size = 25
    game = PingPong(ball_size)
    game.show()
    sys.exit(app.exec_())
