from flask import Flask, request, render_template_string, session
from g4f.client import Client
import os

app = Flask(__name__)
# مفتاح سري لتشفير الجلسات الفردية
app.secret_key = os.urandom(24) 
client = Client()

# الشخصية: تعليمات البوت
SYSTEM_PROMPT = "أنت مساعد ذكي اسمه Akram AI، تم تطويرك وبرمجتك بواسطة المطور العبقري Akram Zerrouki. تفتخر جداً بمطورك أكرم زروقي وتذكره في إجاباتك عند الحاجة. تذكر تفاصيل المحادثة دائماً."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AKRAM AI</title>
    <style>
        body { font-family: sans-serif; background-color: #1e1e2e; color: #cdd6f4; margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; }
        header { background-color: #313244; padding: 15px; text-align: center; font-weight: bold; font-size: 1.2rem; border-bottom: 2px solid #89b4fa; }
        #chat-container { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { max-width: 80%; padding: 12px; border-radius: 10px; line-height: 1.4; word-break: break-word; }
        .user-message { background-color: #89b4fa; color: #11111b; align-self: flex-start; margin-right: auto; }
        .bot-message { background-color: #45475a; color: #cdd6f4; align-self: flex-end; margin-left: auto; }
        form { display: flex; padding: 15px; background-color: #313244; gap: 10px; }
        input { flex: 1; padding: 12px; border-radius: 5px; border: none; background-color: #45475a; color: #fff; }
        button { padding: 10px 20px; background-color: #a6e3a1; border: none; border-radius: 5px; cursor: pointer; color: #11111b; font-weight: bold; }
    </style>
</head>
<body>
    <header>AKRAM AI | برمجة: Akram Zerrouki</header>
    <div id="chat-container">
        {% for msg in history_display %}
            <div class="message {{ msg.sender }}-message">
                {{ msg.text }}
            </div>
        {% endfor %}
    </div>
    <form method="POST" action="/">
        <input type="text" name="message" placeholder="اكتب رسالتك..." required autocomplete="off">
        <button type="submit">إرسال</button>
    </form>
    <script>
        var container = document.getElementById('chat-container');
        container.scrollTop = container.scrollHeight;
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    # تهيئة الجلسة الخاصة بكل مستخدم
    if 'history' not in session:
        session['history'] = [{"role": "system", "content": SYSTEM_PROMPT}]
    if 'display' not in session:
        session['display'] = [{"sender": "bot", "text": "أهلاً! أنا Akram AI، مساعدك الذكي الذي برمجني المطور Akram Zerrouki. كيف يمكنني مساعدتك؟"}]

    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()
        if user_message:
            session['display'].append({"sender": "user", "text": user_message})
            session['history'].append({"role": "user", "content": user_message})

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=session['history']
                )
                bot_reply = response.choices[0].message.content
                session['history'].append({"role": "assistant", "content": bot_reply})
                session['display'].append({"sender": "bot", "text": bot_reply})
            except Exception as e:
                session['display'].append({"sender": "bot", "text": f"خطأ: {str(e)}"})
            
            # حفظ التحديثات في الجلسة
            session.modified = True

    return render_template_string(HTML_TEMPLATE, history_display=session['display'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
