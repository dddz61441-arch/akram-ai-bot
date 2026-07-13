from flask import Flask, request, render_template_string, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AKRAM AI</title>
    <style>
        body { font-family: sans-serif; background-color: #1e1e2e; color: #cdd6f4; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        header { background-color: #313244; padding: 15px; text-align: center; font-weight: bold; }
        #chat-container { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .msg { max-width: 80%; padding: 12px; border-radius: 10px; }
        .user { background-color: #89b4fa; color: #111; align-self: flex-start; }
        .bot { background-color: #45475a; color: #fff; align-self: flex-end; }
        form { display: flex; padding: 15px; background: #313244; gap: 10px; }
        input { flex: 1; padding: 10px; border-radius: 5px; border: none; }
        button { padding: 10px 20px; background: #a6e3a1; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <header>AKRAM AI | برمجة: Akram Zerrouki</header>
    <div id="chat-container"></div>
    <form onsubmit="event.preventDefault(); send();">
        <input id="msg" placeholder="اكتب رسالتك..." required>
        <button type="submit">إرسال</button>
    </form>
    <script>
        let hist = [{"role": "system", "content": "أنت مساعد ذكي اسمه Akram AI، طورك المبرمج أكرم زروقي. كن ودوداً واختصر الإجابات."}];
        function send() {
            let i = document.getElementById('msg');
            let c = document.getElementById('chat-container');
            let m = i.value;
            c.innerHTML += '<div class="msg user">'+m+'</div>';
            hist.push({"role": "user", "content": m});
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({history: hist})
            }).then(r => r.json()).then(d => {
                c.innerHTML += '<div class="msg bot">'+d.reply+'</div>';
                hist.push({"role": "assistant", "content": d.reply});
                i.value = '';
                c.scrollTop = c.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    h = request.json.get('history')
    r = client.chat.completions.create(model="gpt-3.5-turbo", messages=h)
    return jsonify({"reply": r.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
