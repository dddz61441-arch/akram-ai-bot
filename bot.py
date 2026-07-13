from flask import Flask, request, render_template_string, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <body style="background:#1e1e2e; color:#fff; font-family:sans-serif; padding:20px;">
        <h3>Akram AI</h3>
        <div id="chat" style="height:300px; overflow-y:scroll; border:1px solid #444; padding:10px;"></div>
        <input id="msg" style="width:70%; padding:10px;">
        <button onclick="send()" style="padding:10px;">إرسال</button>
        <script>
            function send() {
                let m = document.getElementById('msg').value;
                document.getElementById('chat').innerHTML += '<p>أنت: '+m+'</p>';
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: m})
                }).then(r => r.json()).then(d => {
                    document.getElementById('chat').innerHTML += '<p>البوت: '+d.reply+'</p>';
                });
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_msg}]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "عذراً، حدث خطأ: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
