from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QTimer, Qt, QPropertyAnimation, QPoint
from PySide6.QtGui import QPixmap, QPainter, QBrush, QColor
import vino.resources_rc


class FlyoutBubble(QWidget):
    def __init__(self, parent=None, text=""):
        super().__init__(parent)
        
        # Set window flags to make it a floating widget without a title bar
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Optional for transparency
        
        # Set layout and add a label to display the text
        layout = QHBoxLayout()
        self.label = QLabel(text, self)
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QPixmap(':/icons/check.png').scaled(20, 20))
        layout.addWidget(self.icon_label)
        layout.addWidget(self.label)
        layout.setSpacing(5)
        self.setLayout(layout)
        
        self.setStyleSheet("""color: white;""")
        

    def paintEvent(self, event):
        # Custom paint to draw the rounded rectangle background
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing for smooth corners
        
        # Set the background color and the border radius
        brush = QBrush(QColor(51, 51, 51))  # Equivalent to #333 in hexadecimal
        
        # Apply the brush with the background color
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)  # No border outline
        
        # Draw the rounded rectangle (with a radius of 20)
        rect = self.rect()  # Get the current widget's rectangle
        painter.drawRoundedRect(rect, 20, 20)  # 20px radius for rounded corners
    

    def show_flyout(self, text, animation=True):
        """ Display the flyout bubble with the given text at the top-right corner. """
        self.label.setText(text)  # Set the text in the label

        # Get the parent window's geometry to calculate the position of the flyout
        parent_rect = self.parent().geometry()
        flyout_width = self.sizeHint().width()
        flyout_height = self.sizeHint().height()

        # Position the flyout in the top-right corner of the parent window
        x_pos = parent_rect.right() - flyout_width
        y_pos = parent_rect.top()  

        if animation == True:
            start_x_pos = parent_rect.right()
            start_y_pos = parent_rect.top()  # Same vertical position
            self.move(start_x_pos, start_y_pos)

            end_x_pos = parent_rect.right() - flyout_width
            end_y_pos = parent_rect.top()  # Same vertical position

            self.animation = QPropertyAnimation(self, b"pos")  # Animate the "pos" property
            self.animation.setDuration(200)  # Duration of the animation (in milliseconds)
            self.animation.setStartValue(QPoint(start_x_pos, start_y_pos))  # Start position (off-screen)
            self.animation.setEndValue(QPoint(end_x_pos, end_y_pos))  # End position (on-screen)
            self.animation.start()
        else:
            self.move(x_pos, y_pos)

        self.show()
        QTimer.singleShot(2500, self.hide)


# Another version of flyout bubble, 
# will not block users from saving when the flyout is not disappeared.
# but investigate it later.

# class FlyoutBubble(QWidget):
#     def __init__(self, parent=None, text=""):
#         super().__init__(parent)

#         # Set window flags to make it a child widget without a window frame
#         self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)

#         # Ensure the bubble does not grab focus or block events
#         self.setAttribute(Qt.WA_TransparentForMouseEvents)

#         # Set layout and add a label to display the text and icon
#         layout = QHBoxLayout()
#         self.label = QLabel(text)
#         self.icon_label = QLabel()
#         # Use your actual icon path here
#         self.icon_label.setPixmap(QPixmap(':/icons/check.png').scaled(20, 20))
#         layout.addWidget(self.icon_label)
#         layout.addWidget(self.label)
#         layout.setSpacing(5)
#         layout.setContentsMargins(10, 10, 10, 10)
#         self.setLayout(layout)

#     def paintEvent(self, event):
#         # Custom paint to draw the rounded rectangle background
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing

#         # Set the background color and the border radius
#         brush = QBrush(QColor(51, 51, 51))  # Equivalent to #333
#         painter.setBrush(brush)
#         painter.setPen(Qt.NoPen)  # No border outline

#         # Draw the rounded rectangle
#         rect = self.rect()
#         painter.drawRoundedRect(rect, 20, 20)  # 20px radius for rounded corners

#     def show_flyout(self, text):
#         """Display the flyout bubble with the given text."""
#         self.label.setText(text)

#         # Get the parent window's geometry
#         parent_rect = self.parent().rect()
#         flyout_width = self.sizeHint().width()
#         flyout_height = self.sizeHint().height()

#         # Start position: partially outside the right edge
#         start_x_pos = parent_rect.width() - int(flyout_width * 0.1)  # 10% outside
#         start_y_pos = 20  # Adjust the vertical position as needed
#         self.move(start_x_pos, start_y_pos)

#         # End position: fully visible inside the parent
#         end_x_pos = parent_rect.width() - flyout_width - 20  # 20px margin from the right
#         end_y_pos = start_y_pos

#         # Create an animation to move the flyout bubble
#         self.animation = QPropertyAnimation(self, b"pos")
#         self.animation.setDuration(500)  # Duration in milliseconds
#         self.animation.setStartValue(QPoint(start_x_pos, start_y_pos))
#         self.animation.setEndValue(QPoint(end_x_pos, end_y_pos))
#         self.animation.start()

#         # Show the widget
#         self.show()

#         # Hide after 3 seconds
#         QTimer.singleShot(3000, self.hide)