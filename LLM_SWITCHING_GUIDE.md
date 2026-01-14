# How to Ask Your HVAC Expert Questions

Your HVAC Expert can answer questions using two different "brains":
- **Free Brain** (Ollama) - Good answers, completely free, works offline
- **Premium Brain** (Claude) - Better answers, costs a few cents per question

## 🎯 Quick Guide

### Ask a Free Question (Default)

Just type your question normally:

```bash
hvac "How often should I change my HVAC filter?"
```

**Free! No setup needed!** You already have this working.

### Ask a Premium Question (Optional)

Add `--llm=claude` before your question:

```bash
hvac --llm=claude "How often should I change my HVAC filter?"
```

**Costs about 1-5 cents per question.** Gives more detailed, accurate answers.

## 💰 Cost Comparison

| Type | Cost | Best For |
|------|------|----------|
| **Free (Ollama)** | $0 | Learning, general questions, practice |
| **Premium (Claude)** | ~$0.01-0.05 | Complex problems, critical repairs, professional advice |

## 📋 Which One Should I Use?

### Use the FREE Version When:
- ✅ You're learning about HVAC
- ✅ You have general questions
- ✅ You want to understand how something works
- ✅ You're practicing troubleshooting
- ✅ Cost is a concern

**Examples:**
```bash
hvac "What temperature should I set my thermostat?"
hvac "How does a heat pump work?"
hvac "What is a SEER rating?"
```

### Use the PREMIUM Version When:
- 🔵 You have a complex problem
- 🔵 You need very accurate advice
- 🔵 A repair could be expensive
- 🔵 Safety is a concern
- 🔵 You need professional-level help

**Examples:**
```bash
hvac --llm=claude "My furnace is making strange noises and smells like gas"
hvac --llm=claude "AC won't cool, pressure readings are abnormal"
hvac --llm=claude "Help diagnose expensive compressor issue"
```

## ⚙️ Setting Up Premium (Claude)

The premium version requires a bit of setup:

### Step 1: Get an API Key

1. Go to: https://console.anthropic.com/
2. Sign up for an account (requires credit card)
3. Generate an API key (it starts with `sk-ant-`)
4. Copy the key

### Step 2: Save Your API Key

Run these commands (replace `your-key-here` with your actual key):

```bash
cd /Users/sergevilleneuve/Documents/MyExperiments/HVAC_ideas
echo "ANTHROPIC_API_KEY=your-key-here" > .env.diagnostic
```

### Step 3: Update the System

```bash
# Update your shell
source ~/.zshrc

# Rebuild the system (one time only)
cd /Users/sergevilleneuve/Documents/MyExperiments/opencode
docker compose build
docker compose up -d
```

### Step 4: Test It

```bash
hvac --llm=claude "What is a heat pump?"
```

You should see:
```
🔵 Using Claude API (PAID - ~$0.01-0.05 per session)
```

## 💡 Smart Usage Tips

### Scenario 1: Learning About HVAC

**Use FREE - Learn unlimited for $0:**

```bash
hvac "What are the main parts of an AC unit?"
hvac "How does refrigerant work?"
hvac "What's the difference between a furnace and a heat pump?"
```

### Scenario 2: Simple Troubleshooting

**Use FREE - Common issues:**

```bash
hvac "AC is running but not cooling"
hvac "Thermostat says 'low battery'"
hvac "How to clean my AC filter?"
```

### Scenario 3: Expensive Repair Decision

**Use PREMIUM - Get best advice when money is on the line:**

```bash
hvac --llm=claude "Contractor says I need new compressor for $3000, symptoms are..."
hvac --llm=claude "Strange smell from furnace, intermittent operation, should I be worried?"
```

### Scenario 4: Mixed Approach

**Use both - Free for basics, premium for critical details:**

```bash
# Start with free to understand the problem
hvac "What could cause ice on AC coils?"

# If it's serious, get premium advice
hvac --llm=claude "Detailed steps to diagnose iced AC coils, pressure readings are..."

# Follow-up questions can be free again
hvac "Where is the condensate drain located?"
```

## ❓ Common Questions

### Q: How much does premium cost?

**A:** About 1-5 cents per question. Most questions cost around 2 cents.

### Q: Will it tell me if I'm using premium?

**A:** Yes! You'll see:
- 🟢 = FREE (Ollama)
- 🔵 = PREMIUM (Claude - costs money)

### Q: What if I forget to add `--llm=claude`?

**A:** No worries! It defaults to free. You only pay when you specifically add `--llm=claude`.

### Q: Can I try premium without setup?

**A:** No, but if you try it without setup, it will show you instructions and fall back to free automatically.

### Q: Is the free version good enough?

**A:** Yes! For most questions, the free version is great. Use premium only when you need the absolute best answer.

### Q: How do I know how much I spent?

**A:** Check your Anthropic dashboard at https://console.anthropic.com/ - it shows your usage and costs.

## 🎓 Real World Examples

### Example 1: DIY Homeowner

**John wants to learn about his HVAC system:**

```bash
# All free questions
hvac "How often should I have my HVAC serviced?"
hvac "Can I install a smart thermostat myself?"
hvac "How to prepare my AC for winter?"
hvac "What maintenance can I do myself?"
```

**Cost:** $0

### Example 2: Homeowner with Problem

**Sarah's AC isn't working right:**

```bash
# Start with free to understand
hvac "AC runs but house stays warm"

# Problem seems complex, use premium
hvac --llm=claude "AC compressor cycles on/off every 5 minutes, outside temp 95F, filter clean"

# Follow-up clarification - free is fine
hvac "How do I check refrigerant levels?"
```

**Cost:** ~$0.02 for the one premium question

### Example 3: HVAC Technician

**Mike uses it for complex diagnostics:**

```bash
# Most diagnostics with premium for accuracy
hvac --llm=claude "Customer reports: intermittent heating, error code E3, pilot light stable"
hvac --llm=claude "Heat pump stuck in defrost mode, outdoor temp 25F"

# Quick reference questions can be free
hvac "Standard refrigerant pressure for R-410A?"
```

**Cost:** ~$0.04 for two premium questions

## ⚠️ Important Notes

1. **Free is the default** - You're already using it!
2. **Premium requires setup** - Follow steps above
3. **Premium costs money** - Be mindful when using `--llm=claude`
4. **Both are private** - Free is more private (stays on your computer)
5. **Both are good** - Use free for most things, premium when critical

## 🛠️ Help

### Problem: "Can't find the hvac command"

Try reloading your terminal:
```bash
source ~/.zshrc
```

### Problem: "API key not found" when using premium

Make sure you created the `.env.diagnostic` file:
```bash
cat /Users/sergevilleneuve/Documents/MyExperiments/HVAC_ideas/.env.diagnostic
```

Should show your API key. If not, go back to Step 2 in the setup.

### Problem: Not sure if it's working

Test the free version:
```bash
hvac "test question"
```

Should show: 🟢 Using Ollama (FREE - Local)

---

## 🎯 Bottom Line

**Most people should use the FREE version most of the time.**

Only use premium (`--llm=claude`) when:
- You need professional-level accuracy
- The answer could save you money on repairs
- Safety is a concern
- The problem is very complex

**Remember:**
- Normal question = FREE
- Add `--llm=claude` = PREMIUM (costs pennies)

Happy HVAC troubleshooting! 🔧
