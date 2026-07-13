from flask import Flask, request, render_template_string, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

# هذا القالب يضمن الشكل الجميل والخصوصية
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>AKRAM AI</title>
    <style>
        body { font-family: sans-serif; background-color: #1e1e2e; color: #cdd6f4; margin: 0; height: 100vh; display: flex; flex-direction: column; }
        header { background-color: #313244; padding: 15px; text-align: center; font-weight: bold; }
        #chat { flex: 1; padding: 20px; overflow-y: auto; }
        .msg { padding: 10px; margin: 5px; border-radius: 8px; max-width: 80%; }
        .user { background: #89b4fa; color: #111; align-self: flex-start; }
        .bot { background: #45475a; color: #fff; align-self: flex-end; }
        form { display: flex; padding: 15px; background: #313244; }
        input { flex: 1; padding: 10px; border-radius: 5px; border: none; }
        button { padding: 10px 20px; background: #a6e3a1; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <header>AKRAM AI | برمجة: Akram Zerrouki</header>
    <div id="chat"></div>
    <form onsubmit="event.preventDefault(); send();">
        <input id="msg" placeholder="اكتب رسالتك..." required>
        <button type="submit">إرسال</button>
    </form>
    <script>
        function send() {
            let m = document.getElementById('msg').value;
            let c = document.getElementById('chat');
            c.innerHTML += '<div class="msg user">أنت: '+m+'</div>';
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: m})
            }).then(r => r.json()).then(d => {
                c.innerHTML += '<div class="msg bot">البوت: '+d.reply+'</div>';
                c.scrollTop = c.scrollHeight;
            });
            document.getElementById('msg').value = '';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    # هنا حددنا الموديل ليكون أكثر استقراراً
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"أنت Akram AI، مبرمجك هو أكرم زروقي. أجب على: {user_msg}"}]
    )
    return jsonify({"reply": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

