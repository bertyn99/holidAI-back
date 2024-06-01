from flask import Flask, request, jsonify
from model import ChatBot
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app) 


chatbot = ChatBot()
chatbot.initConv()

@app.route('/map', methods=['GET'])
@cross_origin()
def map():
    print(chatbot.chat.history)
    response = chatbot.send_message("""L'output doit etre sous format, Envoi moi les informations que l'utilisateur t'a donnee dans un format json brut et valide comme ici avec en plus les lieux d'interet que tu lui propose: {
  {
  "trip": {
    "start_date": "12/12/2024",
    "duration": "5 days",
    "budget_per_person": "2000€",
    "interests": ["culture", "food", "shopping"],
    "travelers": 2
  },
  "itinerary": [
    {
      "day": 1,
      "destinations": [
        {
          "name": "Tokyo Tower",
          "address": "4 Chome-2-8 Shibakoen, Minato City, Tokyo 105-0011, Japan",
          "coordinates": {"latitude": 35.6586, "longitude": 139.7454},
          "transport": "Subway - Oedo Line to Akabanebashi Station",
          "ticket_price": "¥900",
          "ticket_link": "https://www.tokyotower.co.jp/en.html",
          "weather": "Average temperature: 10°C, partly cloudy"
        },
        {
          "name": "Roppongi Hills",
          "address": "6 Chome-10-1 Roppongi, Minato City, Tokyo 106-6108, Japan",
          "coordinates": {"latitude": 35.6604, "longitude": 139.7292},
          "transport": "Walk or short subway ride from Tokyo Tower",
          "ticket_price": "Free",
          "ticket_link": "https://www.roppongihills.com/en/",
          "weather": "Average temperature: 10°C, partly cloudy"
        }
      ]
    },
    {
      "day": 2,
      "destinations": [
        {
          "name": "Senso-ji Temple",
          "address": "2 Chome-3-1 Asakusa, Taito City, Tokyo 111-0032, Japan",
          "coordinates": {"latitude": 35.7146, "longitude": 139.7966},
          "transport": "Subway - Ginza Line to Asakusa Station",
          "ticket_price": "Free admission",
          "ticket_link": "https://www.senso-ji.jp/",
          "weather": "Average temperature: 12°C, sunny"
        },
        {
          "name": "Nakamise Shopping Street",
          "address": "Asakusa, Taito City, Tokyo 111-0032, Japan",
          "coordinates": {"latitude": 35.7142, "longitude": 139.7966},
          "transport": "Walk from Senso-ji Temple",
          "ticket_price": "Free",
          "ticket_link": "N/A",
          "weather": "Average temperature: 12°C, sunny"
        },
        {
          "name": "Sumida Aquarium",
          "address": "1-1-2 Oshiage, Sumida City, Tokyo 131-0045, Japan",
          "coordinates": {"latitude": 35.7101, "longitude": 139.8107},
          "transport": "Subway - Hanzomon Line to Oshiage Station",
          "ticket_price": "¥2050",
          "ticket_link": "https://www.sumida-aquarium.com/en/",
          "weather": "Average temperature: 12°C, sunny"
        }
      ]
    },
    {
      "day": 3,
      "destinations": [
        {
          "name": "Shibuya Crossing",
          "address": "2 Chome-2-1 Dogenzaka, Shibuya City, Tokyo 150-0043, Japan",
          "coordinates": {"latitude": 35.6614, "longitude": 139.7041},
          "transport": "JR Yamanote Line to Shibuya Station",
          "ticket_price": "Free",
          "ticket_link": "N/A",
          "weather": "Average temperature: 15°C, clear skies"
        },
        {
          "name": "Shibuya Center-Gai",
          "address": "Udagawacho, Shibuya City, Tokyo 150-0042, Japan",
          "coordinates": {"latitude": 35.6607, "longitude": 139.7004},
          "transport": "Walk from Shibuya Crossing",
          "ticket_price": "Free",
          "ticket_link": "N/A",
          "weather": "Average temperature: 15°C, clear skies"
        },
        {
          "name": "Omotesando Shopping Street",
          "address": "Jingumae, Shibuya City, Tokyo 150-0001, Japan",
          "coordinates": {"latitude": 35.6681, "longitude": 139.7085},
          "transport": "Subway - Ginza Line to Omotesando Station",
          "ticket_price": "Free",
          "ticket_link": "N/A",
          "weather": "Average temperature: 15°C, clear skies"
        }
      ]
    },
    {
      "day": 4,
      "destinations": [
        {
          "name": "Meiji Shrine",
          "address": "1-1 Yoyogikamizonocho, Shibuya City, Tokyo 151-0052, Japan",
          "coordinates": {"latitude": 35.6764, "longitude": 139.6993},
          "transport": "JR Yamanote Line to Harajuku Station",
          "ticket_price": "Free admission",
          "ticket_link": "https://www.meijijingu.or.jp/",
          "weather": "Average temperature: 14°C, partly cloudy"
        },
        {
          "name": "Takeshita Street",
          "address": "1 Chome-17 Jingumae, Shibuya City, Tokyo 150-0001, Japan",
          "coordinates": {"latitude": 35.6704, "longitude": 139.7065},
          "transport": "Walk from Meiji Shrine",
          "ticket_price": "Free",
          "ticket_link": "N/A",
          "weather": "Average temperature: 14°C, partly cloudy"
        },
        {
          "name": "Yoyogi Park",
          "address": "2-1 Yoyogikamizonocho, Shibuya City, Tokyo 151-0052, Japan",
          "coordinates": {"latitude": 35.6717, "longitude": 139.6949},
          "transport": "Walk from Takeshita Street",
          "ticket_price": "Free",
          "ticket_link": "N/A",
          "weather": "Average temperature: 14°C, partly cloudy"
        }
      ]
    },
    {
      "day": 5,
      "destinations": [
        {
          "name": "Tsukiji Fish Market",
          "address": "5 Chome-2-1 Tsukiji, Chuo City, Tokyo 104-0045, Japan",
          "coordinates": {"latitude": 35.6654, "longitude": 139.7707},
          "transport": "Subway - Hibiya Line to Tsukiji Station",
          "ticket_price": "Free admission",
          "ticket_link": "N/A",
          "weather": "Average temperature: 13°C, chance of rain"
        },
        {
          "name": "Ginza Shopping District",
          "address": "Ginza, Chuo City, Tokyo 104-0061, Japan",
          "coordinates": {"latitude": 35.6717, "longitude": 139.7647},
          "transport": "Subway - Hibiya Line to Ginza Station",
          "ticket_price": "Free",
          "ticket_link": "N/A",
          "weather": "Average temperature: 13°C, chance of rain"
        },
        {
          "name": "Kabuki-za Theatre",
          "address": "4 Chome-12-15 Ginza, Chuo City, Tokyo 104-0061, Japan",
          "coordinates": {"latitude": 35.6692, "longitude": 139.7641},
          "transport": "Walk from Ginza Shopping District",
          "ticket_price": "Varies",
          "ticket_link": "https://www.kabukiweb.net/",
          "weather": "Average temperature: 13°C, chance of rain"
        }
      ]
    }
  ]
}

""")
    return response._result.candidates[0].content.parts[0].text

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = chatbot.send_message(data['content'])
    print(response._result.candidates[0].content.parts)
    return response._result.candidates[0].content.parts[0].text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)