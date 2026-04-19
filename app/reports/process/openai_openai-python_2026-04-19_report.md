📊 **项目简报**

**新增功能** 💡

* Add Response.output_as_input helper for manual replay
* Add helpers for reusing Responses output as input
* Add a safe follow-up input helper for Responses output
* Add Response.as_input() helper for stateless follow-ups

**主要改进** 🔧

* Normalize module client base_url trailing slash
* Refresh callable Azure API keys before requests
* Treat empty OPENAI_BASE_URL as unset and fall back to default
* Fix: handle null text values in Response.output_text

**修复问题** 🚀

* Pin setup-rye in GitHub workflows
* Release: 2.32.0, 2.31.0, 2.30.0
* Fix: coerce by_alias=None to False in model_dump to fix TypeError with pydantic v2
* Fix: add client-side validation for shell tool allowlist network policy

Note: The above report is based on the provided pull requests and issues. If you would like me to reorganize or reformat the information, please let me know! 😊