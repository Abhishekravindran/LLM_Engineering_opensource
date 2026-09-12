---
name: fleet-slide
description: House style for turning a fleet research recommendation into a single branded slide. Use when asked to make a slide, deck, or presentation from a research briefing.
---

# Fleet Slide — House Style

You are producing a single-slide summary in the "Voltway Research" brand style
for a fleet-buying recommendation.

## Structure
1. **Title** — a short, punchy statement of the topic (5-8 words)
2. **Key points** — 3 to 5 bullet points, each one short sentence, no jargon
3. **Recommendation** — a single, clear, one-sentence call to action

## Style rules
- Pull the title, key points, and recommendation directly from the source
  briefing markdown file — don't invent facts.
- Keep bullets factual and comparative where possible (numbers, prices,
  ranges) rather than vague ("good value" → "$4,000 cheaper than the
  alternative").
- The recommendation must be a decision, not a summary — "Choose the Model Y"
  not "Both vehicles have strengths."

## Tool to use
Call `create_slide(title, key_points, recommendation)` once you have distilled
the briefing into these three pieces. It handles all layout and branding.
