import json
import os
import re
from flask import Flask, jsonify, render_template_string, request
from google import genai

app = Flask(__name__)

# API Key (କ୍ଲାଉଡ୍ ଏବଂ ଲାପଟପ୍ ଦୁଇଟିଯାକରେ କାମ କରିବ)
API_KEY = os.environ.get(
    "GEMINI_API_KEY", "AQ.Ab8RN6KlrrBbwT_cyqkZJEeB2vHe6JoQRY3sbz193z8nJiyJew"
)
client = genai.Client(api_key=API_KEY)

# 1. ଏଠାରେ ତୁମର ଜରୁରୀ କଣ୍ଟାକ୍ଟ ନମ୍ବର ସେଭ୍ କର
CONTACTS = {
    "rajesh": "9876543210",
    "papa": "9876543211",
    "mummy": "9876543212",
    "home": "9876543213",
}

# 2. ମୋବାଇଲ୍ ଆପ୍ ଗୁଡ଼ିକର ଅଫିସିଆଲ୍ Package Name ଲିଷ୍ଟ୍
APPS = {
    "whatsapp": "com.whatsapp",
    "youtube": "com.google.android.youtube",
    "instagram": "com.instagram.android",
    "facebook": "com.facebook.katana",
    "chrome": "com.android.chrome",
    "maps": "com.google.android.apps.maps",
    "gmail": "com.google.android.gm",
    "phonepe": "com.phonepe.app",
    "paytm": "net.one97.paytm",
    "gpay": "com.google.android.apps.nbu.paisa.user",
    "spotify": "com.spotify.music",
    "telegram": "org.telegram.messenger",
    "flipkart": "com.flipkart.android",
    "amazon": "in.amazon.mShop.android.shopping",
    "camera": "com.android.camera",
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#111111">
    <title>Max AI</title>
    <style>
        body { background: #111; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }
        #status { font-size: 19px; color: #00ffcc; margin: 15px 0; }
        #box { background: #222; padding: 15px; border-radius: 15px; min-height: 160px; font-size: 18px; text-align: left; margin-bottom: 15px; }
        button { padding: 12px 22px; font-size: 17px; background: #00ffcc; color: #000; border: none; border-radius: 10px; font-weight: bold; margin: 5px; cursor: pointer; }
        select { padding: 10px; font-size: 16px; border-radius: 10px; background: #222; color: #00ffcc; border: 1px solid #00ffcc; margin-bottom: 10px; }
        input { padding: 12px; font-size: 16px; width: 62%; border-radius: 10px; border: none; }
    </style>
</head>
<body>
    <h2>🤖 Max - AI Assistant</h2>
    
    <div>
        <label>भाषा / ଭାଷା: </label>
        <select id="langSelect" onchange="changeLang()">
            <option value="hi-IN">हिन्दी (Hindi)</option>
            <option value="or-IN">ଓଡ଼ିଆ (Odia)</option>
        </select>
    </div>

    <button id="startBtn" onclick="startAll()">Start Voice Assistant</button>
    <div id="status">ऊपर बटन दबाएं / ବଟନ୍ ଦବାନ୍ତୁ</div>
    <div id="box"></div>

    <div>
        <input type="text" id="textInput" placeholder="यहाँ लिखें / ଏଠାରେ ଲେଖନ୍ତୁ...">
        <button onclick="sendText()">Send</button>
    </div>

    <script>
        const statusDiv = document.getElementById('status');
        const box = document.getElementById('box');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition;
        let currentLang = 'hi-IN';

        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = currentLang;
            recognition.interimResults = false;

            recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                askMax(text);
            };

            recognition.onerror = (event) => {
                statusDiv.innerText = "⚠️ Mic Error: " + event.error;
            };
        }

        function changeLang() {
            currentLang = document.getElementById('langSelect').value;
            if (recognition) recognition.lang = currentLang;
        }

        function startAll() {
            document.getElementById('startBtn').style.display = 'none';
            if (currentLang === 'or-IN') {
                bolo("ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କ ମ୍ୟାକ୍ସ। ମୁଁ ଆପଣଙ୍କର କ'ଣ ସାହାଯ୍ୟ କରିପାରିବି?");
            } else {
                bolo("Namaste! Main aapka Max hoon. Main aapki kya madad kar sakta hoon?");
            }
        }

        function suno() {
            if (!recognition) return;
            statusDiv.innerText = currentLang === 'or-IN' ? "🎤 ଶୁଣୁଛି... କୁହନ୍ତୁ" : "🎤 सुन रहा हूँ... बोलिए";
            try { recognition.start(); } catch(e) {}
        }

        function sendText() {
            const input = document.getElementById('textInput');
            if (input.value.trim() !== "") {
                askMax(input.value);
                input.value = "";
            }
        }

        async function askMax(text) {
            box.innerHTML = "<p><b>You:</b> " + text + "</p>";
            statusDiv.innerText = currentLang === 'or-IN' ? "⏳ ଭାବୁଛି..." : "⏳ सोच रहा हूँ...";

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: text, lang: currentLang})
            });
            const data = await res.json();
            box.innerHTML += "<p style='color:#00ffcc'><b>Max:</b> " + data.answer + "</p>";
            
            bolo(data.answer, data);
        }

        function performAction(data) {
            const action = data.action;
            const target = data.target || "";
            const msg = data.message || "";

            if (action === "call" && target) {
                window.location.href = "tel:" + target;
            } else if (action === "whatsapp_msg" && target) {
                window.location.href = "https://wa.me/91" + target + "?text=" + encodeURIComponent(msg);
            } else if (action === "open_app" && target) {
                window.location.href = "intent://#Intent;package=" + target + ";end";
            } else if (action === "youtube") {
                window.open(target ? "https://www.youtube.com/results?search_query=" + encodeURIComponent(target) : "https://www.youtube.com", "_blank");
            } else if (action === "maps" && target) {
                window.open("https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(target), "_blank");
            } else if (action === "google" && target) {
                window.open("https://www.google.com/search?q=" + encodeURIComponent(target), "_blank");
            }
        }

        function bolo(text, data = null) {
            statusDiv.innerText = currentLang === 'or-IN' ? "🔊 କହୁଛି..." : "🔊 बोल रहा हूँ...";
            const speech = new SpeechSynthesisUtterance(text);
            speech.lang = currentLang;
            speech.onend = () => {
                if (data) performAction(data);
                suno();
            };
            window.speechSynthesis.speak(speech);
        }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/ask", methods=["POST"])
def ask():
    try:
        q = request.json.get("question", "")
        lang = request.json.get("lang", "hi-IN")
        lang_instruction = (
            "ଓଡ଼ିଆ (Odia script) ଭାଷାରେ"
            if lang == "or-IN"
            else "सरल हिंदी भाषा में"
        )

        prompt = f"""
        आपका नाम Max है और आप एक स्मार्ट मोबाइल AI असिस्टेंट हैं।
        सेव किए गए कॉन्टैक्ट्स: {json.dumps(CONTACTS)}
        उपलब्ध मोबाइल ऐप्स: {json.dumps(APPS)}
        यूजर का कमांड: "{q}"

        कमांड को समझकर केवल नीचे दिए गए JSON फॉर्मेट में ही उत्तर दें:
        {{
            "answer": "छोटा और स्पष्ट जवाब {lang_instruction} दें",
            "action": "call" या "whatsapp_msg" या "open_app" या "youtube" या "maps" या "google" या "none",
            "target": "अगर call या whatsapp_msg है तो 10 अंकों का फोन नंबर; अगर open_app है तो पैकेज नाम; अगर youtube/maps/google है तो सर्च शब्द; अन्यथा खाली",
            "message": "अगर whatsapp_msg है तो भेजा जाने वाला मैसेज (अन्यथा खाली)"
        }}
        """
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite", contents=prompt
        )
        raw_text = re.sub(
            r"^```json\s*|\s*```$", "", response.text.strip()
        )
        result = json.loads(raw_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "answer": "क्षमा करें, कुछ समस्या आई है।",
            "action": "none",
            "target": "",
            "message": "",
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)