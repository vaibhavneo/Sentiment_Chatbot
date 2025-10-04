# --------------------------------------------
# Added for environment-backed configuration:
# DefaultConfig reads secrets from environment
# so API keys and endpoints are not hard-coded.
# --------------------------------------------
import os

class DefaultConfig:
    # These pull from environment variables if present.
    # Windows (cmd):   SET MicrosoftAIServiceEndpoint=...
    # Windows (PowerShell):   $env:MicrosoftAIServiceEndpoint="..."
    # macOS/Linux (bash/zsh): export MicrosoftAIServiceEndpoint=...
    API_KEY = os.environ.get("MicrosoftAPIKey")
    ENDPOINT_URI = os.environ.get("MicrosoftAIServiceEndpoint")

    # Optional: you can put other app settings here, too.
    PORT = int(os.environ.get("PORT", "5000"))
