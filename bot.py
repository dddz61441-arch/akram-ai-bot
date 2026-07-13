from flask import Flask, request, render_template_string, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

SYSTEM_PROMPT = "أنت مساعد ذكي اسمه Akram AI، تم تطويرك وبرمجتك بواسطة المطور العبقري Akram Zerrouki. تفتخر جداً بمطورك أكرم زروقي. تذكر تفاصيل المحادثة دائماً."

# HTML يحتوي على منطق حفظ المحادثة في متصفح المستخدم فقط
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>AKRAM AI</title>
    <style>
        body { font-family: sans-serif; background-color: #1e1e2e; color: #cdd6f4; margin: 0; padding: 20px; }
        #chat-container { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
        .message { padding: 10px; border-radius: 8px; max-width: 80%; }
        .user { background: #89b4fa; color: #111; align-self: flex-start; }
        .bot { background: #45475a; color: #fff; align-self: flex-end; }
    </style>
</head>
<body>
    <header><h1>AKRAM AI | برمجة: Akram Zerrouki</h1></header>
    <div id="chat-container"></div>
    <input id="msg" placeholder="اكتب رسالتك...">
    <button onclick="send()">إرسال</button>
    <script>
        let history = [{"role": "system", "content": "{{system_prompt}}"}];
        function send() {
            let m = document.getElementById('msg').value;
            let c = document.getElementById('chat-container');
            c.innerHTML += '<div class="message user">'+m+'</div>';
            history.push({"role": "user", "content": m});
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({history: history})
            }).then(r => r.json()).then(d => {
                c.innerHTML += '<div class="message bot">'+d.reply+'</div>';
                history.push({"role": "assistant", "content": d.reply});
            });
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE, system_prompt=SYSTEM_PROMPT)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    history = data.get('history')
    response = client.chat.completions.create(model="gpt-4o", messages=history)
    return jsonify({"reply": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
