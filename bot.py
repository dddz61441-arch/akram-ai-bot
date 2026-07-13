from flask import Flask, request, render_template_string
from g4f.client import Client

app = Flask(__name__)
client = Client()

# الشخصية: تعليمات سرية للبوت
SYSTEM_PROMPT = "أنت مساعد ذكي اسمه Akram AI، تم تطويرك وبرمجتك بواسطة Akram Zerrouki. تفتخر جداً بمطورك أكرم زروقي. تذكر تفاصيل المحادثة دائماً."

# الذاكرة الحقيقية (لإرسالها للذكاء الاصطناعي)
history = [{"role": "system", "content": SYSTEM_PROMPT}]

# نسخة العرض (للواجهة فقط)
display_messages = [{"sender": "bot", "text": "أهلاً! أنا Akram AI، مساعدك الذكي الذي برمجني المطور Akram Zerrouki. كيف يمكنني مساعدتك؟"}]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AKRAM AI</title>
    <style>
        body { font-family: sans-serif; background-color: #1e1e2e; color: #cdd6f4; margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; }
        header { background-color: #313244; padding: 15px; text-align: center; font-weight: bold; font-size: 1.2rem; }
        #chat-container { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { max-width: 80%; padding: 12px; border-radius: 10px; line-height: 1.4; word-break: break-word; }
        .user-message { background-color: #89b4fa; color: #11111b; align-self: flex-start; }
        .bot-message { background-color: #45475a; color: #cdd6f4; align-self: flex-end; }
        form { display: flex; padding: 15px; background-color: #313244; gap: 10px; }
        input { flex: 1; padding: 12px; border-radius: 5px; border: none; background-color: #45475a; color: #fff; }
        button { padding: 10px 20px; background-color: #a6e3a1; border: none; border-radius: 5px; cursor: pointer; color: #11111b; font-weight: bold; }
    </style>
</head>
<body>
    <header>AKRAM AI | برمجة: Akram Zerrouki</header>
    <div id="chat-container">
        {% for msg in display_messages %}
            <div class="message {% if msg.sender == 'user' %}user-message{% else %}bot-message{% endif %}">
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
    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()
        if user_message:
            display_messages.append({"sender": "user", "text": user_message})
            history.append({"role": "user", "content": user_message})

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=history
                )
                bot_reply = response.choices[0].message.content

                history.append({"role": "assistant", "content": bot_reply})
                display_messages.append({"sender": "bot", "text": bot_reply})

            except Exception as e:
                display_messages.append({"sender": "bot", "text": f"خطأ: {str(e)}"})

    return render_template_string(HTML_TEMPLATE, display_messages=display_messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
