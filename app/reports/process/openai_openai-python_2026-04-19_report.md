**简报**

🔴 **新增功能**
Add Response.output_as_input for multi-turn follow-ups (#3032)
Add a safe follow-up input helper for Responses output (#3028)
Add Response.as_input() helper for stateless follow-ups (#3029)

🟠 **主要改进**
Treat empty OPENAI_BASE_URL as unset and fall back to default (#3058)
Handle null text values in Response.output_text (#3057)
Add docstrings to parsing helpers and streaming events (#3046)

🔵 **修复问题**
fix(structured outputs): resolve memory leak in parse methods (#2860)
Fix vision example to use Chat Completions API (#2904)
Refresh callable Azure API keys before requests (#2992)
Normalize module client base_url trailing slash (#2990)
Add aclose alias to AsyncStream (#2996)
fix: coerce by_alias=None to False in model_dump to fix TypeError with pydantic v2 (#2999)
fix: treat empty OPENAI_BASE_URL env var as unset to restore default fallback (#3001)

🟡 **其他**
Pin GitHub Actions workflow references (#3021)
release: 2.32.0 (#3074), 2.31.0 (#3020), 2.30.0 (#2995)