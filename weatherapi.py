import sys
import os
from dotenv import load_dotenv
import requests
from PyQt5.QtWidgets import (QApplication, QWidget,QLabel,
                             QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt

class Weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label= QLabel('Enter the city name: ',self)
        self.city_input=QLineEdit(self)
        self.get_weather_button=QPushButton('Get weather: ',self)
        self.label_temperature=QLabel(self)
        self.label_emoji=QLabel(self)
        self.label_description=QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather Forecast App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.label_temperature)
        vbox.addWidget(self.label_emoji)
        vbox.addWidget(self.label_description)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.label_temperature.setAlignment(Qt.AlignCenter)
        self.label_description.setAlignment(Qt.AlignCenter)
        self.label_emoji.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.label_temperature.setObjectName("label_temperature")
        self.label_emoji.setObjectName("label_emoji")
        self.label_description.setObjectName("label_description")

        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size:45px;
                font-style:italic;
            }
            QLineEdit#city_input{
                font-size:40px;
            }
            QPushButton#get_weather_button{
                font-size:30px;
                font-weight:Bold;
            }
            QLabel#label_temperature{
                font-size:65px;  
            }
            QLabel#label_emoji{
                font-size:90px;
                font-family:Segoe UI emoji; 
            }
            QLabel#label_description{
                font-size:55px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        load_dotenv()
        api_key = os.getenv("OPENWEATHER_API_KEY")

        if not api_key:
            self.display_error("API Key not found.\nPlease set it in .env file.")
            return

        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()

            if data["cod"]==200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API KEY")
                case 403:
                    self.display_error("Forbidden:\nAccess denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Service unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nRequest get timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n{req_error}")

    def display_error(self,message):
        self.label_temperature.setStyleSheet('font-size:35px;')
        self.label_temperature.setText(message)
        self.label_emoji.clear()
        self.label_description.clear()

    def display_weather(self,data):
        self.label_temperature.setStyleSheet('font-size:60px;')
        temp_k=data["main"]["temp"]
        temp_c=temp_k-273.15
        weather_id=data["weather"][0]["id"]
        weather_info=data["weather"][0]["description"]

        print(data)
        self.label_temperature.setText(f"{temp_c:.0f}°C")
        self.label_emoji.setText(self.display_weather_emoji(weather_id))
        self.label_description.setText(weather_info)

    @staticmethod
    def display_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 700 <= weather_id <= 741:
            return "🌫️"
        elif weather_id==762:
            return "🌋"
        elif weather_id==771:
            return "💨"
        elif weather_id==781:
            return "🌪️"
        elif weather_id==800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == "__main__":
    app=QApplication(sys.argv)
    weather_app= Weatherapp()
    weather_app.show()
    sys.exit(app.exec_())