/**
 * CAELUM AI Assistant Backend
 *
 * This connects your AI Assistant to Claude API
 * Run with: node backend-api.js
 *
 * Installation:
 * 1. npm init -y
 * 2. npm install express cors dotenv @anthropic-ai/sdk
 * 3. Create .env file with: ANTHROPIC_API_KEY=your_key_here
 * 4. Run: node backend-api.js
 * 5. Update assistant.html sendMessage() to call http://localhost:3001/api/assistant
 */

const express = require('express');
const cors = require('cors');
require('dotenv').config();
const Anthropic = require("@anthropic-ai/sdk");

const app = express();
app.use(express.json());
app.use(cors());
app.use(express.static('.')); // Serve static files from current directory

const client = new Anthropic();

// Blueprint context for the AI
const BLUEPRINT_CONTEXT = `
You are the Sovereign Assistant, an expert guide helping users master the AI Agency Blueprint.

You have deep knowledge of:
- Starting an AI agency with no code/experience
- Finding clients via Google Maps local targeting
- 17 specific no-code AI tools (ChatGPT, Zapier, Make.com, Manychat, Tidio, GHL, Notion AI, Canva AI, ElevenLabs, HeyGen, Typeform, Calendly, Buffer, Loom, Airtable, Synthesia, Webflow)
- Cold calling scripts that convert
- Service pricing from $300-$3000
- Building recurring revenue models
- Client outreach strategies
- Automation workflows

Your responses should:
1. Be confident but not arrogant
2. Provide actionable, specific advice
3. Reference the blueprint when relevant
4. Encourage sovereign thinking and quick action
5. Keep answers concise (200-400 words)
6. Ask clarifying questions if needed
7. Suggest immediate action steps

Tone: Direct, empowering, strategic. Think like a mentor.
`;

// Serve index.html for root path
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Main chat endpoint
app.post('/api/assistant', async (req, res) => {
  try {
    const { message, topic } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Build system prompt with topic context
    let topicContext = '';
    switch(topic) {
      case 'module1':
        topicContext = 'The user is asking about Module 1: The Foundation - understanding AI agency work.';
        break;
      case 'module2':
        topicContext = 'The user is asking about Module 2: Finding Clients using the Google Maps method.';
        break;
      case 'module3':
        topicContext = 'The user is asking about Module 3: The 17 no-code AI tools to deliver services.';
        break;
      case 'module4':
        topicContext = 'The user is asking about Module 4: Getting Paid - pricing and recurring revenue.';
        break;
      case 'coldcall':
        topicContext = 'The user is asking about cold calling scripts, objection handling, or outreach strategies.';
        break;
      case 'pricing':
        topicContext = 'The user is asking about pricing strategy, service packages, or packaging. Recommend: Starter ($300-500), Growth ($800-1200), Sovereign ($1500-2500).';
        break;
      default:
        topicContext = 'The user has a general question about the blueprint.';
    }

    // Call Claude
    const response = await client.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 500,
      system: BLUEPRINT_CONTEXT + '\n\n' + topicContext,
      messages: [
        {
          role: "user",
          content: message
        }
      ]
    });

    // Extract the response
    const assistantMessage = response.content[0].type === 'text'
      ? response.content[0].text
      : 'Unable to process response';

    res.json({
      response: assistantMessage,
      tokens_used: response.usage.output_tokens
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      error: 'Failed to process request',
      message: error.message
    });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'Assistant API running' });
});

// Start server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`🤖 Sovereign Assistant API running on http://localhost:${PORT}`);
  console.log(`📍 POST /api/assistant - Chat with AI`);
  console.log(`💚 GET /health - Health check`);
});
