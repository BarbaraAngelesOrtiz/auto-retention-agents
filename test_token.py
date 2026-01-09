from dotenv import load_dotenv
load_dotenv()
from agents.ms_graph_agent import get_access_token
token = get_access_token()
print(token)
