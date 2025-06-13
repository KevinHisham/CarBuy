from ariadne import make_executable_schema, graphql_sync
from ariadne.asgi import GraphQL
import uvicorn
import os
from database import init_db
from resolvers import query, mutation
from seed import seed_data

# Load GraphQL schema
def load_schema():
    with open('schema.graphql', 'r') as file:
        return file.read()

type_defs = load_schema()
schema = make_executable_schema(type_defs, query, mutation)

# Initialize database
init_db()

# Seed data if database is empty
seed_data()

# Create GraphQL app
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)