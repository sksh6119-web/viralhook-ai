import streamlit as st
import streamlit.components.v1 as components

# পেজ লেআউট পুরো স্ক্রিন জুড়ে করার জন্য
st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini AI Assistant</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 20px;
            background: #ffffff;
            border-bottom: 1px solid #e9ecef;
            width: 100%;
            flex-shrink: 0;
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
            padding: 12px 16px;
            text-align: center;
            font-size: 15px;
            font-weight: 600;
            text-decoration: none;
            display: block;
            width: 100%;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            flex-shrink: 0;
        }
        #chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            padding-bottom: 120px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
        }
        .message {
            max-width: 85%;
            padding: 16px 20px;
            border-radius: 20px;
            font-size: 16px;
            line-height: 1.6;
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
            margin-top: 12px;
            border-top: 1px solid #f1f3f4;
            padding-top: 10px;
        }
        .speak-btn {
            background: #e8f0fe;
            border: 1px solid #d2e3fc;
            border-radius: 20px;
            padding: 8px 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 15px;
            font-weight: 600;
            color: #1a73e8;
        }
        /* পুরো স্ক্রিন জুড়ে নিচে চওড়া ভাসমান ইনপুট বক্স */
        .input-bar {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 92%;
            max-width: 850px;
            background: #ffffff;
            border-radius: 32px;
            padding: 10px 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            border: 1px solid #dadce0;
            display: flex;
            align-items: center;
            gap: 12px;
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
            width: 44px;
            height: 44px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
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
            হ্যালো! 😊 আমি আপনার এআই সহকারী। যারা পড়তে পারেন না বা শুনতে চান, তারা ডানপাশের "ভয়েস শুনুন" বাটনে ক্লিক করলেই আমি পুরো লেখা মুখে পড়ে শোনাবো! ✨
            <div class="toolbar">
                <button class="speak-btn" onclick="toggleSpeech(this, 'হ্যালো! 😊 আমি আপনার এআই সহকারী। যারা পড়তে পারেন না বা শুনতে চান, তারা ডানপাশের ভয়েস শুনুন বাটনে ক্লিক করলেই আমি পুরো লেখা মুখে পড়ে শোনাবো!')">🔊 ভয়েস শুনুন</button>
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
            
            if (sender === 'user') {
                msgDiv.innerText = text;
            } else {
                msgDiv.innerHTML = text;
            }
            
            chatContainer.appendChild(msgDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            if (!text) return;

            appendMessage(text, 'user');
            input.value = '';

            // এআই উত্তর জেনারেট করা
            const aiResponse = "আপনার প্রশ্নের উত্তর দেওয়া হলো। এটি অত্যন্ত চমৎকার একটি বিষয়!";
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

        function toggleSpeech(btn, text) {
            if (!('speechSynthesis' in window)) {
                alert('আপনার ব্রাউজার ভয়েস সাপোর্ট করে না।');
                return;
            }

            // যদি ইতিমধ্যে কথা বলতে থাকে তবে থামিয়ে দেবো
            if (window.speechSynthesis.speaking) {
                window.speechSynthesis.cancel();
                btn.style.background = '#e8f0fe';
                btn.style.color = '#1a73e8';
                btn.innerHTML = '🔊 ভয়েস শুনুন';
                return;
            }

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
    </script>
</body>
</html>
"""

# Streamlit কম্পোনেন্টে পুরো স্ক্রিন হাইট (850px) দিয়ে রেন্ডার করা
components.html(html_code, height=850, scrolling=False)
