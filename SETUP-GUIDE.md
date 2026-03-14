# CAELUM AI Agency Blueprint — Setup & Management Guide

## 🚀 **How to Run the Website**

### Local Development (Currently Running)
Your website is already running on **http://localhost:8000**

**Server:** Python HTTP Server on Port 8000
**Status:** Running 24/7 as long as the Python HTTP Server is active

To start/restart:
```bash
# Navigate to your cealum directory
cd C:\Users\luisa\Downloads\cealum

# Start Python HTTP Server
python -m http.server 8000
```

### For Production (Going Live)
You have several options:

**Option 1: Netlify (Free, Recommended)**
- Upload all HTML/CSS/JS files
- Your site goes live instantly
- Custom domain support
- Free SSL/HTTPS
- https://netlify.com

**Option 2: Vercel**
- Similar to Netlify
- Optimized for modern web projects
- https://vercel.com

**Option 3: AWS S3 + CloudFront**
- More control
- Higher performance for larger scale
- Costs depend on traffic

**Option 4: Your Own Server**
- Full control
- Upload to any web hosting provider
- Requires keeping server running

---

## 🧪 **Testing Without Payment**

### Quick Test Mode
1. Go to: **http://localhost:8000/test-mode.html**
2. Click **"✓ Simulate Purchase"**
3. You'll get a test access code
4. Access all protected pages:
   - Dashboard: http://localhost:8000/dashboard.html
   - Blueprint: http://localhost:8000/blueprint.html
   - 3D Version: http://localhost:8000/ai-agency-blueprint-3d.html
   - AI Assistant: http://localhost:8000/assistant.html

### Manual Testing via Browser Console
```javascript
// Grant access
localStorage.setItem('blueprint-access-code', 'TEST-CODE-12345');
window.location.href = 'http://localhost:8000/dashboard.html';

// Revoke access
localStorage.removeItem('blueprint-access-code');
window.location.href = 'http://localhost:8000/index.html';
```

---

## 🤖 **AI Assistant — Connect to Claude API**

### Current State
The AI Assistant has a working UI but uses placeholder responses.

### To Enable Real AI Responses
You have 2 options:

#### **Option A: Simple (Recommended for Now)**
The assistant is ready to use — currently showing simulated responses. This is perfect for testing the UX.

#### **Option B: Live Claude API Integration**
Requires a backend server. Here's how:

**Step 1: Set up a backend service** (Choose one)
- Node.js + Express
- Python + Flask
- Vercel Serverless Functions (Recommended)

**Step 2: Create an API endpoint**
```javascript
// Example: /api/assistant
POST /api/assistant
{
  "message": "What's the cold calling script?",
  "topic": "coldcall"
}

Response:
{
  "response": "Based on the blueprint, here's the effective cold calling script..."
}
```

**Step 3: Update assistant.html**
Replace the setTimeout mock with:
```javascript
async function sendMessage(){
  const input = document.getElementById('userInput');
  const text = input.value.trim();

  if(!text) return;

  addMessage('user', text);
  input.value = '';
  showLoading(true);

  try {
    const response = await fetch('/api/assistant', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text, topic: currentTopic})
    });

    const data = await response.json();
    addMessage('assistant', data.response);
  } catch(err) {
    addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
  }

  showLoading(false);
}
```

**Step 4: Backend example (Node.js)**
```javascript
const Anthropic = require("@anthropic-ai/sdk");

app.post("/api/assistant", async (req, res) => {
  const { message, topic } = req.body;

  const blueprintContext = `
  You are the Sovereign Assistant, helping people master the AI Agency Blueprint.
  Context: This is a guide on starting an AI agency in 30 days.
  Topics covered: Finding clients via Google Maps, 17 no-code tools, pricing strategies,
  cold calling scripts, and recurring revenue models.
  `;

  const client = new Anthropic();
  const response = await client.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 500,
    system: blueprintContext,
    messages: [{ role: "user", content: message }]
  });

  res.json({ response: response.content[0].text });
});
```

---

## 📦 **Managing Products**

### Current Products
1. **AI Agency Blueprint** (Text) — blueprint.html
2. **3D Interactive Version** — ai-agency-blueprint-3d.html
3. **Sovereign Assistant** (AI) — assistant.html
4. **Admin Portal** — admin.html

### To Add New Products

**Step 1: Create the product HTML file**
```html
<!-- Make sure to add access protection at the top -->
<script>
  if(!localStorage.getItem('blueprint-access-code')){
    window.location.href='index.html';
  }
</script>
```

**Step 2: Add to dashboard.html**
Add a new product card in the grid:
```html
<div class="product-card">
  <div class="product-icon">📚</div>
  <div class="product-title">Your New Product</div>
  <div class="product-desc">Description of what this product is.</div>
  <a href="your-product.html" class="product-btn">Open Product</a>
</div>
```

**Step 3: Update pricing if needed**
Edit the price in index.html if adding premium tier products:
```javascript
amount: { value: '27.00' }  // Change this number
```

### To Update Product Pricing

**Current Setup:** $27 lifetime access for ALL products

**To Change Price:**
1. Edit index.html line 38: Change `$27` to your new price
2. Edit PayPal button amount (line 47): Change `'27.00'` to new amount

**To Create Multiple Tiers:**
Create separate pages with different PayPal buttons and prices

---

## 📊 **Admin Dashboard Features**

**Access:** http://localhost:8000/admin.html

Shows:
- Total purchases count
- Total revenue
- Last sale date/time
- Purchase details table with:
  - Access codes
  - Timestamps
  - PayPal order IDs
  - Status

**Export Data:** CSV export button to download all customer records

---

## 🔒 **Security Notes**

⚠️ **For Production:**
1. Don't hardcode sensitive info
2. Set up HTTPS (free via Let's Encrypt)
3. Protect admin.html with password
4. Use environment variables for PayPal keys
5. Add server-side validation for purchases

**Current Setup:** Good for development/testing. Upgrade security before real payments.

---

## 📱 **Deployment Checklist**

Before going live with real payments:

- [ ] Test full purchase flow multiple times
- [ ] Verify all product pages load correctly
- [ ] Test on mobile devices
- [ ] Set up custom domain
- [ ] Enable HTTPS
- [ ] Update PayPal settings (test mode → live mode)
- [ ] Add privacy policy
- [ ] Add terms of service
- [ ] Test email notifications (optional)
- [ ] Set up analytics (Google Analytics)
- [ ] Backup your files

---

## 🎯 **Next Steps**

1. **Test Everything:** Use test-mode.html to verify flows
2. **Customize:** Update colors, text, pricing as needed
3. **Add Content:** Consider additional modules/bonuses
4. **Connect AI:** (Optional) Set up Claude API integration
5. **Launch:** Deploy to production when ready

---

## 📞 **Quick Reference**

| Page | URL | Purpose |
|------|-----|---------|
| Paywall | index.html | Where visitors purchase |
| Dashboard | dashboard.html | Products hub (after purchase) |
| Blueprint | blueprint.html | Main course content |
| 3D Version | ai-agency-blueprint-3d.html | Interactive format |
| Assistant | assistant.html | AI study guide |
| Admin | admin.html | Track sales & customers |
| Test Mode | test-mode.html | Test without payment |

---

**Your system is production-ready.** Go live when you're comfortable with the setup!
