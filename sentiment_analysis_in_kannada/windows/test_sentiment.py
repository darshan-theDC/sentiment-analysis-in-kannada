import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(os.path.join(project_root, 'utils'))

from PyQt5.QtCore import Qt, QTimer, QUrl, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from model_utils import SentimentModel  # Make sure to import your sentiment model

class SentimentTestWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI components
        self.init_ui()

        # Initialize the SentimentModel
        self.model = SentimentModel()

        # Initialize Media Player for sound effects
        self.media_player = QMediaPlayer()

    def init_ui(self):
        # Load the Orbitron font
        font_path = os.path.join("C:/Users/dcdar/OneDrive/Documents/5th sem mini project/sentiment_analysis_in_kannada/assets/fonts/Orbitron/Orbitron.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)

        # Check if the font was loaded successfully
        if font_id == -1:
            print("Font could not be loaded.")
            self.setFont(QFont("Arial"))
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family))

        # Set up the window with futuristic look
        self.setWindowTitle('Sentiment Analysis in Kannada')
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("background-color: #121212; color: white; font-family: 'Orbitron';")

        # Layout
        layout = QVBoxLayout()

        # Text input for user
        self.input_label = QLabel("Enter text for sentiment analysis:")
        self.input_label.setStyleSheet("font-size: 16px; color: #00b0ff;")
        self.text_input = QLineEdit()
        self.text_input.setStyleSheet("font-size: 18px; padding: 10px; background-color: #222222; color: white; border-radius: 8px;")
        layout.addWidget(self.input_label)
        layout.addWidget(self.text_input)

        # Analyze sentiment button
        self.analyze_button = QPushButton("Analyze Sentiment")
        self.analyze_button.setStyleSheet("""
            font-size: 16px;
            background-color: #00b0ff;
            color: white;
            border-radius: 15px;
            padding: 10px;
        """)
        self.analyze_button.clicked.connect(self.analyze_sentiment)
        layout.addWidget(self.analyze_button)

        # Output label for displaying sentiment
        self.output_label = QLabel("Sentiment will appear here.")
        self.output_label.setStyleSheet("font-size: 18px; color: #00b0ff;")
        layout.addWidget(self.output_label)

        # Dynamic sentiment icons (initially hidden)
        self.sentiment_icon = QLabel()
        layout.addWidget(self.sentiment_icon)

        # Set the layout for the window
        self.setLayout(layout)

    def analyze_sentiment(self):
        # Get the text from input field
        input_text = self.text_input.text()

        # Get sentiment from model
        sentiment = self.model.predict_sentiment(input_text)

        # Display sentiment in output label
        self.output_label.setText(f"Sentiment: {sentiment}")

        # Show the corresponding icon and play sound
        if sentiment == "Positive":
            self.show_positive()
        else:
            self.show_negative()

    def show_positive(self):
        icon_path = os.path.join("C:/Users/dcdar/OneDrive/Documents/5th sem mini project/sentiment_analysis_in_kannada/assets/icons", "positive.png")
        self.sentiment_icon.setPixmap(QPixmap(icon_path))
        self.sentiment_icon.setAlignment(Qt.AlignCenter)
        self.sentiment_icon.setStyleSheet("background-color: #00ff00; border-radius: 25px; padding: 10px;")

        # Play positive sound
        self.play_sound("positive_sound.mp3")

        # Add glow effect using QGraphicsDropShadowEffect
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setColor(Qt.green)  # Glow color
        glow_effect.setBlurRadius(15)  # The intensity of the glow
        glow_effect.setOffset(0, 0)  # Glow in all directions
        self.sentiment_icon.setGraphicsEffect(glow_effect)

    def show_negative(self):
        icon_path = os.path.join("C:/Users/dcdar/OneDrive/Documents/5th sem mini project/sentiment_analysis_in_kannada/assets/icons", "negative.png")
        self.sentiment_icon.setPixmap(QPixmap(icon_path))
        self.sentiment_icon.setAlignment(Qt.AlignCenter)
        self.sentiment_icon.setStyleSheet("background-color: #ff3333; border-radius: 25px; padding: 10px;")

        # Play negative sound
        self.play_sound("negative_sound.wav")

        # Add glow effect using QGraphicsDropShadowEffect
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setColor(Qt.red)  # Glow color
        glow_effect.setBlurRadius(15)  # The intensity of the glow
        glow_effect.setOffset(0, 0)  # Glow in all directions
        self.sentiment_icon.setGraphicsEffect(glow_effect)

    def play_sound(self, sound_file):
        """Play the given sound file."""
        sound_path = os.path.join("C:/Users/dcdar/OneDrive/Documents/5th sem mini project/sentiment_analysis_in_kannada/assets/sounds", sound_file)
        if not os.path.exists(sound_path):
            print(f"Error: Sound file does not exist at {sound_path}")
            return
        sound_url = QUrl.fromLocalFile(sound_path)  # Convert the file path to QUrl
        self.media_player.setMedia(QMediaContent(sound_url))
        self.media_player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SentimentTestWindow()
    window.show()
    sys.exit(app.exec_())