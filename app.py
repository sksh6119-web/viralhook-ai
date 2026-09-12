import streamlit.components.v1 as components

# জেমিনির হুবহু ইন্টারফেস, ভাসমান ইনপুট এবং পারফেক্ট ভয়েস কন্ট্রোল সিস্টেমসহ HTML/JS অ্যাপ
html_code = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini AI Assistant</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 20px;
            background: #ffffff;
            border-bottom: 1px solid #e9ecef;
        }
        h2 {
            margin: 0;
            color: #202124;
            font-size: 20px;
            font-weight: 500;
        }
        select {
            padding: 6px 12px;
            border-radius: 12px;
            border: 1px solid #dadce0;
            background: #f8f9fa;
            font-size: 14px;
            outline: none;
        }
        .ad-banner {
            background: linear-gradient(135deg, #4285f4, #34a853);
            color: white;
            padding: 10px 16px;
            text-align: center;
            font-size: 14px;
            font-weight: 500;
            text-decoration: none;
            display: block;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        #chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            padding-bottom: 120px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
        }
        .message {
            max-width: 85%;
            padding: 14px 18px;
            border-radius: 18px;
            font-size: 16px;
            line-height: 1.5;
            word-wrap: break-word;
        }
        .user-message {
            background: #e8f0fe;
            color: #202124;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }
        .ai-message {
            background: #ffffff;
            color: #202124;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }
        .toolbar {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 12px;
            margin-top: 10px;
            border-top: 1px solid #f1f3f4;
            padding-top: 8px;
        }
        .speak-btn {
            background: #e8f0fe;
            border: 1px solid #d2e3fc;
            border-radius: 20px;
            padding: 6px 14px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            font-weight: 500;
            color: #1a73e8;
        }
        /* একদম নিচে চওড়া ভাসমান ইনপুট বক্স */
        .input-bar {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 85%;
            max-width: 750px;
            background: #ffffff;
            border-radius: 32px;
            padding: 8px 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
            border: 1px solid #dadce0;
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 9999;
        }
        .input-bar input {
            flex: 1;
            border: none;
            outline: none;
            font-size: 16px;
            padding: 8px;
            background: transparent;
            color: #202124;
        }
        .input-bar button {
            background: #1a73e8;
            border: none;
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
    </style>
</head>
<body>

    <header>
        <h2>✨ Gemini AI</h2>
        <select id="voiceGender">
            <option value="Female">Female Voice</option>
            <option value="Male">Male Voice</option>
        </select>
    </header>

    <a href="https://www.profitableratecpmnetwork.com/txpfccym?key=16ed7712c3ae7b7b8d90efb5c53300b3" target="_blank" class="ad-banner">
        🚀 বিশেষ অফার ও আপডেট দেখতে এখানে ক্লিক করুন! (Sponsored)
    </a>

    <div id="chat-container">
        <div class="message ai-message">
            হ্যালো! 😊 আমি আপনার এআই সহকারী। আজ আপনাকে কীভাবে সাহায্য করতে পারি? বলতে পারেন, আমি শোনার জন্য প্রস্তুত আছি! ✨
            <div class="toolbar">
                <button class="speak-btn" onclick="toggleSpeech(this, 'হ্যালো! 😊 আমি আপনার এআই সহকারী। আজ আপনাকে কীভাবে সাহায্য করতে পারি? বলতে পারেন, আমি শোনার জন্য প্রস্তুত আছি! ✨')">🔊 ভয়েস শুনুন</button>
            </div>
        </div>
    </div>

    <div class="input-bar">
        <input type="text" id="userInput" placeholder="Gemini-কে কিছু জিজ্ঞাসা করুন..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">⬆</button>
    </div>

    <script>
        const apiKey = "gsk_v1Wv65vW5g5W5vW5g5W5vW5g5W5vW5g5W5vW5g5W5vW5g5W5"; // আপনার Groq API Key এখানে সেট করা হবে বা সিক্রেট থেকে আসবে
        
        function appendMessage(text, sender) {
            const chatContainer = document.getElementById('chat-container');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender === 'user' ? 'user-message' : 'ai-message'}`;
            
            if (sender === 'user') {
                msgDiv.innerText = text;
            } else {
                msgDiv.innerHTML = text;
                // অটো ভয়েস রিডিং যারা পড়তে পারেন না তাদের জন্য
                playTextAudio(text);
            }
            
            chatContainer.appendChild(msgDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        async function sendMessage() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            if (!text) return;

            appendMessage(text, 'user');
            input.value = '';

            // এআই রিপ্লাইয়ের সিমুলেশন বা গ্রোক এপিআই কল
            const aiResponse = "আপনার কথার উত্তর দিচ্ছি বন্ধু। বলুন আর কী জানতে চান?";
            
            const gender = document.getElementById('voiceGender').value;
            const safeTextJson = JSON.stringify(aiResponse);
            
            const aiHTML = `${aiResponse}
                <div class="toolbar">
                    <button class="speak-btn" onclick="toggleSpeech(this, ${safeTextJson})">🔊 ভয়েস শুনুন</button>
                </div>`;
            
            appendMessage(aiHTML, 'ai');
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        }

        let currentUtterance = null;
        function toggleSpeech(btn, text) {
            if (!('speechSynthesis' in window)) {
                alert('আপনার ব্রাউজার ভয়েস সাপোর্ট করে না।');
                return;
            }

            if (window.speechSynthesis.speaking) {
                window.speechSynthesis.cancel();
                btn.style.background = '#e8f0fe';
                btn.style.color = '#1a73e8';
                btn.innerHTML = '🔊 ভয়েস শুনুন';
                return;
            }

            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'bn-IN';
            msg.rate = 1.0;
            
            var gender = document.getElementById('voiceGender').value;
            var filter = gender === 'Female' ? 'female' : 'male';
            
            var voices = window.speechSynthesis.getVoices();
            for(var v = 0; v < voices.length; v++) {
                if(voices[v].name.toLowerCase().includes(filter) || voices[v].lang.includes('bn')) {
                    msg.voice = voices[v];
                    break;
                }
            }

            msg.onend = function() {
                btn.style.background = '#e8f0fe';
                btn.style.color = '#1a73e8';
                btn.innerHTML = '🔊 ভয়েস শুনুন';
            };

            btn.style.background = '#fce8e6';
            btn.style.color = '#c5221f';
            btn.innerHTML = '🔇 বন্ধ করুন';
            
            window.speechSynthesis.speak(msg);
        }

        function playTextAudio(text) {
            // যারা পড়তে পারেন না তাদের জন্য অটো ট্রিগার ভয়েস
            if ('speechSynthesis' in window) {
                var cleanText = text.replace(/<[^>]*>?/gm, ''); // HTML ট্যাগ রিমুভ করার জন্য
                var msg = new SpeechSynthesisUtterance(cleanText);
                msg.lang = 'bn-IN';
                window.speechSynthesis.speak(msg);
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=800, scrolling=True)
