import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="wide")

perfect_app_code = """
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
            padding: 14px 24px;
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
            padding-bottom: 150px;
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
        /* জলজল বা পাল্সিং অ্যানিমেশনসহ প্রিমিয়াম ভয়েস বাটন */
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
        .speak-btn.active {
            background: #fce8e6;
            color: #c5221f;
            border-color: #fadcbc;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(197, 34, 31, 0.4); }
            70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(197, 34, 31, 0); }
            100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(197, 34, 31, 0); }
        }
        /* নিচে চওড়া ভাসমান কম্বো ইনপুট বার */
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
        .mic-btn {
            background: #f1f3f4;
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: #5f6368;
            transition: 0.2s;
        }
        .mic-btn.listening {
            background: #fce8e6;
            color: #c5221f;
            animation: pulse 1.5s infinite;
        }
        .send-btn {
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
            flex-shrink: cent;
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
            নমস্কার! 😊 আমি আপনার জেমিনি সহকারী। যারা পড়তে পারেন না, তারা নিচের ডানপাশের "🔊 ভয়েস শুনুন" বাটনে ক্লিক করলেই জলজল করে অ্যানিমেশন সহ পুরো লেখাটি মুখে পড়ে শোনাবো। বলুন, আপনাকে কীভাবে সাহায্য করতে পারি? ✨
            <div class="toolbar">
                <button class="speak-btn" id="btn_welcome" onclick="playVoice(this, 'নমস্কার! আমি আপনার জেমিনি সহকারী। যারা পড়তে পারেন না, তারা নিচের ডানপাশের ভয়েস শুনুন বাটনে ক্লিক করলেই পুরো লেখাটি মুখে পড়ে শোনাবো। বলুন, আপনাকে কীভাবে সাহায্য করতে পারি?')">🔊 ভয়েস শুনুন</button>
            </div>
        </div>
    </div>

    <div class="input-bar">
        <button class="mic-btn" id="micBtn" title="মুখে বলুন" onclick="startSpeechRecognition()">🎙️</button>
        <input type="text" id="userInput" placeholder="Gemini-কে কিছু জিজ্ঞাসা করুন..." onkeypress="handleKeyPress(event)">
        <button class="send-btn" onclick="sendMessage()">⬆</button>
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

            appendMessage(text, 'user');
            input.value = '';

            setTimeout(() => {
                const aiResponse = "আপনার কথাটি আমি অত্যন্ত মনোযোগ দিয়ে শুনেছি। এটি একটি দারুণ বিষয় এবং আমি আপনাকে এতে পুরোপুরি সাহায্য করতে প্রস্তুত আছি!";
                const safeTextJson = JSON.stringify(aiResponse);
                const uniqueId = 'btn_' + Date.now();
                
                const aiHTML = `${aiResponse}
                    <div class="toolbar">
                        <button class="speak-btn" id="${uniqueId}" onclick="playVoice(this, ${safeTextJson})">🔊 ভয়েস শুনুন</button>
                    </div>`;
                
                appendMessage(aiHTML, 'ai');
            }, 500);
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        }

        // ব্রাউজারের ভয়েস স্পিচ রিকগনিশন (মুখে বলে টাইপ করার জন্য)
        function startSpeechRecognition() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert('আপনার ব্রাউজার ভয়েস টাইপিং সাপোর্ট করে না।');
                return;
            }

            const recognition = new SpeechRecognition();
            recognition.lang = 'bn-IN';
            const micBtn = document.getElementById('micBtn');

            recognition.onstart = function() {
                micBtn.classList.add('listening');
                micBtn.innerHTML = '🔴';
            };

            recognition.onresult = function(event) {
                const speechToText = event.results[0][0].transcript;
                document.getElementById('userInput').value = speechToText;
                micBtn.classList.remove('listening');
                micBtn.innerHTML = '🎙️';
                sendMessage();
            };

            recognition.onerror = function() {
                micBtn.classList.remove('listening');
                micBtn.innerHTML = '🎙️';
            };

            recognition.onend = function() {
                micBtn.classList.remove('listening');
                micBtn.innerHTML = '🎙️';
            };

            recognition.start();
        }

        // ১০০% পারফেক্ট সাউন্ড ও জলজল করা অ্যানিমেশনসহ ভয়েস প্লে সিস্টেম
        function playVoice(btn, text) {
            if (!('speechSynthesis' in window)) {
                alert('আপনার ব্রাউজার ভয়েস সাপোর্ট করে না।');
                return;
            }

            // যদি অলরেডি কথা বলতে থাকে তবে বন্ধ করবে
            window.speechSynthesis.cancel();

            // সব বাটনের একটিভ স্টাইল রিমুভ করা
            document.querySelectorAll('.speak-btn').forEach(b => {
                b.classList.remove('active');
                b.innerHTML = '🔊 ভয়েস শুনুন';
            });

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
                btn.classList.add('active');
                btn.innerHTML = '🔊 বলছি... (জলজল করছে)';
            };

            msg.onend = function() {
                btn.classList.remove('active');
                btn.innerHTML = '🔊 ভয়েস শুনুন';
            };

            msg.onerror = function() {
                btn.classList.remove('active');
                btn.innerHTML = '🔊 ভয়েস শুনুন';
            };

            window.speechSynthesis.speak(msg);
        }
    </script>
</body>
</html>
"""

components.html(perfect_app_code, height=900, scrolling=False)
