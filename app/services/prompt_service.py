def create_titles_prompt(data):
    return f"""
Generate 5 YouTube video titles based on these requirements:

Topic: {data.topic}
Target audience: {data.target_audience.value}
Language: {data.language.value}
Duration: {data.duration} minutes
Content type: {data.content_type.value}
Tone: {data.tone.value}
Additional instructions: {data.instructions or "None"}

Requirements:
- Generate exactly 5 titles.
- Titles must be relevant to the topic.
- Match the requested language.
- Match the target audience and tone.
- Make them engaging but not misleading.
- Do not use fake claims, exaggerated promises, or clickbait.
- Return only the 5 titles, one per line.
"""


def create_hooks_prompt(data):
    return f"""
Generate 3 YouTube video opening hooks based on these requirements:

Topic: {data.topic}
Target audience: {data.target_audience.value}
Language: {data.language.value}
Duration: {data.duration} minutes
Content type: {data.content_type.value}
Tone: {data.tone.value}
Additional instructions: {data.instructions or "None"}

Requirements:
- Generate exactly 3 hooks.
- Hook 1 must be a question-based hook.
- Hook 2 must be a short storytelling-based hook.
- Hook 3 must be a curiosity-based hook.
- Match the requested language.
- Match the target audience and tone.
- Make the hooks natural and engaging.
- Do not use fake claims or misleading statements.
- Do not invent personal experiences, real events, quotes, statistics, or claims; if using a story format, make it clearly hypothetical.
- Keep each hook concise and suitable for spoken YouTube content.
- Return only the 3 hooks, one per line.
"""


def create_outline_prompt(data):
    return f"""
Create a clear YouTube video outline based on these requirements:

Topic: {data.topic}
Target audience: {data.target_audience.value}
Language: {data.language.value}
Duration: {data.duration} minutes
Content type: {data.content_type.value}
Tone: {data.tone.value}
Additional instructions: {data.instructions or "None"}

Requirements:
- Create a logical structure for the entire video.
- Include an introduction.
- Include the main sections needed to explain the topic clearly.
- Include a conclusion.
- Include a natural CTA section.
- Match the requested language, audience, content type, and tone.
- Keep the number of sections appropriate for the requested video duration.
- Do not invent facts, statistics, quotes, or research.
- Avoid presenting subjective or absolute claims as facts.
- Prefer neutral, accurate wording such as "beginner-friendly" instead of claims like "the easiest" or "the best."
- Return only the outline items, one per line.
"""



def create_script_prompt(data, selected_title, selected_hook, outline):
    return f"""
Write a complete YouTube video script based on the following requirements.

Video topic: {data.topic}
Target audience: {data.target_audience.value}
Language: {data.language.value}
Target duration: {data.duration} minutes
Content type: {data.content_type.value}
Tone: {data.tone.value}
Additional instructions: {data.instructions or "None"}

Selected title:
{selected_title}

Selected hook:
{selected_hook}

Approved outline:
{outline}

Requirements:
- Write a natural, spoken YouTube script.
- Start with the selected hook.
- Follow the approved outline in the same logical order.
- Structure the script using clear, separate section headings.
- Put each section heading on its own line.
- Use exactly this heading format: [INTRODUCTION], [MAIN CONTENT: section title], [CONCLUSION AND CTA].
- Put the selected hook at the beginning of [INTRODUCTION].
- Give every main topic from the approved outline its own [MAIN CONTENT: section title] heading, replacing section title with the actual topic.
- Keep each main section's spoken script under its heading.
- Put the final summary and call to action inside [CONCLUSION AND CTA].
- Never repeat the introduction heading at the end.
- Do not create an extra section after [CONCLUSION AND CTA].
- Leave a blank line between each heading and section.
- Use smooth transitions between sections.
- Explain concepts clearly for the target audience.
- Include useful examples where appropriate.
- When the topic involves programming, include short, runnable code examples where useful.
- Explain each code example in simple, beginner-friendly language.
- Show the expected output for code examples.
- Explain what the output means.
- For non-programming topics, include relevant practical examples or demonstrations where useful.
- Keep examples accurate, relevant to the topic, and easy for beginners to follow.
- End with a clear conclusion and natural CTA.
- Match the requested language and tone.
- Do not invent statistics, quotes, research, personal experiences, or factual claims.
- Avoid absolute or exaggerated claims such as "the best", "the easiest", "the most", or similar statements unless they are clearly supported.
- Prefer neutral, accurate wording such as "beginner-friendly" or "widely used".
- If a factual claim may require verification, clearly mark it for verification.
- Do not include stage directions unless they are genuinely useful for the spoken script.
- Do not add a separate title, word count, or duration estimate.
- Target approximately {data.duration * 130} spoken words for the requested {data.duration}-minute video.
- Use approximately 130 spoken words per minute.
- Keep the final script reasonably close to this target word count.
- Return only the complete script.
"""



def create_visuals_prompt(data):
    return f"""
Generate visual suggestions for this YouTube video.

Video topic: {data.topic}
Target audience: {data.target_audience.value}
Language: {data.language.value}
Duration: {data.duration} minutes
Content type: {data.content_type.value}
Tone: {data.tone.value}

Selected title:
{data.selected_title}

Final script:
{data.script}

Requirements:
- Create visual suggestions for each major section of the script.
- Each suggestion must include:
  1. Section
  2. Visual
  3. B-roll
  4. On-screen text
- Visual suggestions must directly match what is being discussed in the script.
- Suggest practical visuals that a YouTube creator could realistically produce or find.
- Do not generate images or videos.
- Do not invent facts, statistics, quotes, or events.
- Keep suggestions clear and concise.
- Match the requested language where appropriate.
- Avoid unnecessary visual suggestions for every single sentence.
- Return one JSON object, not a JSON array.
- The JSON object must contain a top-level "visuals" key whose value is an array.
- Each item in "visuals" must contain exactly these fields:
  "section", "visual", "b_roll", "on_screen_text".
- Do not include Markdown, code fences, explanations, or any text outside the JSON.
"""


def create_description_prompt(data):
    return f"""
Create a professional YouTube video description based on the following information.

Video topic: {data.topic}
Target audience: {data.target_audience.value}
Language: {data.language.value}
Duration: {data.duration} minutes
Content type: {data.content_type.value}
Tone: {data.tone.value}

Selected title:
{data.selected_title}

Final script:
{data.script}

Requirements:
- Write an engaging but natural YouTube description.
- The intro should briefly tell viewers what they will learn.
- The summary should accurately summarize the video.
- Topics should contain the main subjects covered in the video.
- Keywords should be relevant search terms, not keyword stuffing.
- Generate relevant hashtags.
- Create a natural CTA encouraging viewers to engage with the channel.
- Match the requested language and tone.
- Do not invent facts, statistics, quotes, or claims.
- Do not make exaggerated promises.
- Base the description strictly on the provided script.
- Return valid JSON only.
- The JSON must contain exactly these fields:
  "intro",
  "summary",
  "topics",
  "keywords",
  "hashtags",
  "cta".
- "topics", "keywords", and "hashtags" must be arrays of strings.
- Do not include Markdown, code fences, explanations, or text outside the JSON.
"""


def create_regeneration_prompt(data):
    return f"""
Regenerate only one section of a YouTube video script.

Video topic: {data.topic}
Target audience: {data.target_audience.value}
Language: {data.language.value}
Duration: {data.duration} minutes
Content type: {data.content_type.value}
Tone: {data.tone.value}
Additional instructions: {data.instructions or "None"}

Selected title:
{data.selected_title}

Section to regenerate:
{data.section_name}

Current section:
{data.current_section}

Full script for context:
{data.full_script}

Requirements:
- Rewrite only the requested section.
- Preserve the overall topic, language, audience, and tone.
- Keep the regenerated section consistent with the rest of the script.
- Improve clarity, flow, and natural spoken delivery.
- Do not rewrite or return the other sections.
- Do not invent statistics, quotes, research, personal experiences, or factual claims.
- Avoid exaggerated or absolute claims.
- Do not add a separate title or explanation.
- Return only the regenerated section text.
"""