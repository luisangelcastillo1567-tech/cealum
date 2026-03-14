# 🤖 Connect AI Assistant to Claude API

Your AI Assistant currently uses placeholder responses. Here's how to add **real AI**.

---

## **Step 1: Get Claude API Key**

1. Go to https://console.anthropic.com
2. Sign up / Log in
3. Click "API Keys" → "Create Key"
4. Copy your API key (keep it secret!)
5. Save it somewhere safe

**Cost:** $0.003 per 1K input tokens, $0.015 per 1K output tokens
- Each user question ≈ $0.001
- At 1000 questions/month = ~$1

---

## **Step 2: Set Up Backend**

### Option A: Node.js (Local Development)

**1. Install Node.js**
- Download from https://nodejs.org
- Choose LTS version
- Follow installer

**2. Set Up Backend**
```bash
cd C:\Users\luisa\Downloads\cealum

# Install dependencies
npm install

# Create .env file with your API key
# Windows Command Prompt:
echo ANTHROPIC_API_KEY=sk-ant-xxx... > .env

# Or create .env file manually and paste:
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

**3. Start the API Server**
```bash
npm start
# Should show: "🤖 Sovereign Assistant API running on http://localhost:3001"
```

### Option B: Deploy to Vercel (Cloud - Free!)

**1. Push code to GitHub**
```bash
git init
git add .
git commit -m "Add AI assistant"
git push origin main
```

**2. Connect to Vercel**
- Go to https://vercel.com
- Click "New Project"
- Import GitHub repo
- Add environment variable:
  - Key: `ANTHROPIC_API_KEY`
  - Value: `sk-ant-xxxxx` (your API key)
- Click "Deploy"

**Your API is now live at:** `https://your-project.vercel.app/api/assistant`

---

## **Step 3: Update Assistant Frontend**

Update the `sendMessage()` function in assistant.html:

**Current (Mock) Code:**
```javascript
async function sendMessage(){
  const input = document.getElementById('userInput');
  const text = input.value.trim();
  if(!text) return;
  addMessage('user', text);
  input.value = '';
  showLoading(true);

  // Mock response
  setTimeout(() => {
    addMessage('assistant', 'Mock response...');
    showLoading(false);
  }, 1000);
}
```

**New (Real AI) Code:**
```javascript
async function sendMessage(){
  const input = document.getElementById('userInput');
  const text = input.value.trim();
  if(!text) return;
  addMessage('user', text);
  input.value = '';
  showLoading(true);

  try {
    // Call your backend API
    const response = await fetch('http://localhost:3001/api/assistant', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        message: text,
        topic: currentTopic
      })
    });

    const data = await response.json();
    addMessage('assistant', data.response);
  } catch(err) {
    addMessage('assistant', 'Unable to connect to AI. Please try again.');
  }

  showLoading(false);
}
```

---

## **For Production (Already Live Site)**

If your site is already deployed to Netlify:

**1. Deploy backend separately** (Option: Vercel)
```bash
# Push only backend-api.js and package.json to separate repo
# Deploy to Vercel (as above)
```

**2. Update API URL in assistant.html**
```javascript
const response = await fetch('https://your-project.vercel.app/api/assistant', {
  // ... rest of code
});
```

**3. No frontend redeploy needed** (if you edit via Netlify)

---

## **Testing the AI**

### Local Test
```bash
# Terminal 1: Start backend
npm start

# Terminal 2: Open in browser
http://localhost:8000/assistant.html

# Type a question and send!
```

### Production Test
1. Visit your live site
2. Go to the AI Assistant
3. Ask a question
4. Should get real AI response from Claude

---

## **Example Questions Users Can Ask**

```
"What's the first step to find clients?"
→ AI explains Google Maps method

"How much should I charge for a chatbot?"
→ AI gives pricing recommendations

"Give me a cold calling script"
→ AI provides word-for-word script

"How do I structure recurring revenue?"
→ AI explains retainer models

"Which tool should I use for automation?"
→ AI recommends specific tools
```

---

## **Costs Breakdown**

### Development (Free)
- Node.js: Free
- Vercel: Free tier included
- 100 free API calls/month: Free

### Monthly (At Scale)
- 1000 users asking 1 question each = ~$1 (Claude API)
- Vercel bandwidth: Free tier usually sufficient
- Domain: $1-12/month
- **Total: ~$2-13/month**

### Revenue Example
- 1000 users × $27 = $27,000
- Claude AI cost: ~$10
- **Profit: $26,990**

---

## **Troubleshooting**

### "API key error"
- Check .env file has correct key
- No spaces around `=` sign
- Restart the server after updating .env

### "Cannot connect to localhost:3001"
- Make sure `npm start` is running
- Check firewall isn't blocking port 3001
- Try different port in backend-api.js

### "CORS error"
- Backend has `cors` enabled
- Make sure backend is running
- Check API URL is correct

### "AI response is slow"
- First request takes ~2-3 seconds (Claude warming up)
- Subsequent requests are faster
- This is normal

---

## **Advanced: Custom System Prompts**

In `backend-api.js`, modify `BLUEPRINT_CONTEXT` to customize AI behavior:

```javascript
const BLUEPRINT_CONTEXT = `
You are the Sovereign Assistant...
[Edit this text to change how AI responds]
`;
```

Examples:
- Make responses longer/shorter
- Change tone (more formal/casual)
- Add specific company info
- Include special instructions

---

## **Going Even Further**

### Add Conversation History
```javascript
// Keep previous messages in context
const conversationHistory = [];

// Add to message before sending
messages: [
  ...conversationHistory,
  { role: "user", content: message }
]
```

### Add Fine-Tuning
```javascript
// Train Claude on your specific data
// See: https://docs.anthropic.com/en/docs/build/finetuning
```

### Add Voice Input
```javascript
// Use Web Speech API for voice questions
// User speaks → AI responds with text/voice
```

---

## **Quick Start Checklist**

- [ ] Get Claude API key from console.anthropic.com
- [ ] Install Node.js
- [ ] Run `npm install` in cealum folder
- [ ] Create `.env` with API key
- [ ] Run `npm start`
- [ ] Update assistant.html with new code
- [ ] Test in browser
- [ ] Deploy backend to Vercel
- [ ] Update API URL for production
- [ ] Live! 🎉

---

**Need help?** Check the comments in backend-api.js or Anthropic docs at https://docs.anthropic.com

Your AI assistant is ready to power up! 🚀
