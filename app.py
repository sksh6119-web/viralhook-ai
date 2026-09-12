import streamlit as st
import streamlit.components.v1 as components

# পেজ কনফিগারেশন
st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="wide")

# শতভাগ নিখুঁত এবং ফিক্সড ফুল-স্ক্রিন HTML/JS অ্যাপ কোড
html_app_code = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini AI Assistant</title>
    <style>
        * { box-sizing: border-box; }
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            background-color: #f0f4f9;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 24px;
            background: #ffffff;
            border-bottom: 1px solid #e1e6ed;
            width: 100%;
            flex-shrink: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        h2 {
            margin: 0;
            color: #1f1f1f;
            font-size: 22px;
            font-weight: 600;
        }
        select {
            padding: 8px 14px;
            border-radius: 12px;
            border: 1px solid #dcdfe5;
            background: #f8f9fa;
            font-size: 14px;
            outline: none;
            font-weight: 500;
            cursor: pointer;
        }
        .ad-banner {
            background: linear-gradient(135deg, #1a73e8, #34a853);
            color: white;
            padding: 14px 20px;
            text-align: center;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            display: block;
            width: 100%;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            flex-shrink: 0;
        }
        #chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            padding-bottom: 140px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
        }
        .message {
            max-width: 85%;
            padding: 18px 22px;
            border-radius: 24px;
            font-size: 17px;
            line-height: 1.7;
            word-wrap: break-word;
        }
        .user-message {
            background: #d3e3fd;
            color: #041e49;
            align-self: flex-end;
            border-bottom-right-radius: 6px;
            font-weight: 500;
        }
        .ai-message {
            background: #ffffff;
            color: #202124;
            align-self: flex-start;
            border-bottom-left-radius: 6px;
            border: 1px solid #e1e6ed;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        }
        .toolbar {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 12px;
            margin-top: 14px;
            border-top: 1px solid #f1f3f4;
            padding-top: 12px;
        }
        .speak-btn {
            background: #e8f0fe;
            border: 1px solid #d2e3fc;
            border-radius: 28px;
            padding: 10px 22px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 16px;
            font-weight: 600;
            color: #1a73e8;
            transition: all 0.2s ease;
        }
        .speak-btn:active {
            transform: scale(0.95);
        }
        /* একদম নিচে চওড়া ভাসমান প্রিমিয়াম ইনপুট বক্স */
        .input-bar {
            position: fixed;
            bottom: 25px;
            left: 50%;
            transform: translateX(-50%);
            width: 92%;
            max-width: 850px;
            background: #ffffff;
            border-radius: 36px;
            padding: 10px 22px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            border: 1px solid #dcdfe5;
            display: flex;
            align-items: center;
            gap: 14px;
            z-index: 9999;
        }
        .input-bar input {
            flex: 1;
            border: none;
            outline: none;
            font-size: 17px;
            padding: 10px;
            background: transparent;
            color: #202124;
        }
        .input-bar button {
            background: #1a73e8;
            border: none;
            color: white;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
            box-shadow: 0 4px 10px rgba(26,115,232,0.3);
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
            নমস্কার! 😊 আমি আপনার জেমিনি সহকারী। যারা পড়তে পারেন না, তারা নিচের ডানপাশের "🔊 ভয়েস শুনুন" বাটনে ক্লিক করলেই আমি পুরো লেখাটি মুখে পড়ে শোনাবো। বলুন, আপনাকে কীভাবে সাহায্য করতে পারি? ✨
            <div class="toolbar">
                <button class="speak-btn" onclick="playVoice(this, 'নমস্কার! 😊 আমি আপনার জেমিনি সহকারী। যারা পড়তে পারেন না, তারা নিচের ডানপাশের ভয়েস শুনুন বাটনে ক্লিক করলেই আমি পুরো লেখাটি মুখে পড়ে শোনাবো। বলুন, আপনাকে কীভাবে সাহায্য করতে পারি?')">🔊 ভয়েস শুনুন</button>
            </div>
        </div>
    </div>

    <div class="input-bar">
        <input type="text" id="userInput" placeholder="Gemini-কে কিছু জিজ্ঞাসা করুন..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">⬆</button>
    </div>

    <script>
        function appendMessage(text, sender) {
            const chatContainer = document.getElementById('chat-container');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender === 'user' ? 'user-message' : 'ai-message'}`;
            msgDiv.innerHTML = text;
            chatContainer.appendChild(msgDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            if (!text) return;

            // యూজার মেসেজ প্রদর্শন
            appendMessage(text, 'user');
            input.value = '';

            // এআই উত্তরের সিমুলেশন বা রেসপন্স
            setTimeout(() => {
                const aiResponse = "আপনার কথাটি আমি বুঝতে পেরেছি। এটি অত্যন্ত চমৎকার একটি বিষয় এবং আমি আপনাকে এতে পূর্ণ সহযোগিতা করব!";
                const safeTextJson = JSON.stringify(aiResponse);
                
                const aiHTML = `${aiResponse}
                    <div class="toolbar">
                        <button class="speak-btn" onclick="playVoice(this, ${safeTextJson})">🔊 ভয়েস শুনুন</button>
                    </div>`;
                
                appendMessage(aiHTML, 'ai');
            }, 500);
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        }

        // ব্রাউজারের নেটিভ ভয়েস স্পিচ ইঞ্জিন
        function playVoice(btn, text) {
            if (!('speechSynthesis' in window)) {
                alert('আপনার ব্রাউজার ভয়েস সাপোর্ট করে না।');
                return;
            }

            window.speechSynthesis.cancel();

            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'bn-IN';
            msg.rate = 0.95;
            
            var gender = document.getElementById('voiceGender').value;
            var filter = gender === 'Female' ? 'female' : 'male';
            
            var voices = window.speechSynthesis.getVoices();
            for(var v = 0; v < voices.length; v++) {
                if(voices[v].name.toLowerCase().includes(filter) || voices[v].lang.includes('bn')) {
                    msg.voice = voices[v];
                    break;
                }
            }

            msg.onstart = function() {
                btn.style.background = '#fce8e6';
                btn.style.color = '#c5221f';
                btn.innerHTML = '🔊 বলছি...';
            };

            msg.onend = function() {
                btn.style.background = '#e8f0fe';
                btn.style.color = '#1a73e8';
                btn.innerHTML = '🔊 ভয়েস শুনুন';
            };

            msg.onerror = function() {
                btn.style.background = '#e8f0fe';
                btn.style.color = '#1a73e8';
                btn.innerHTML = '🔊 ভয়েস শুনুন';
            };

            window.speechSynthesis.speak(msg);
        }
    </script>
</body>
</html>
"""

# Streamlit কম্পোনেন্টে পুরো স্ক্রিন জুড়ে রেন্ডার করা
components.html(html_app_code, height=900, scrolling=False)
