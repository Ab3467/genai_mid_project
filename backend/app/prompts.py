import json

SYSTEM_PROMPT = """You are an expert software engineer and code reviewer.
Return ONLY valid JSON with fields:
- summary: one-sentence summary.
- potential_issues: list of {line: [start,end] or null, severity: "low|medium|high", issue: "<short>", explanation: "<why>", suggested_fix: "<code or steps>"}.
- suggestions: list of short strings.
- score: integer 0-100.
Return strict JSON only.
"""

def make_user_prompt(code: str, language: str, depth: str, context):
    ctx = context or "None"
    return f"""Language: {language}
Review depth: {depth}
Context: {ctx}

Code:
```{language}
{code}
```"""
