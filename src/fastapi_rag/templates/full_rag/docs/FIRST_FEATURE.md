# Build Your First Feature

This tutorial shows how to add a simple `projects` feature to the template.

The goal is to help a junior developer or intern learn the architecture by building a real feature in the correct way.

By the end, you should understand:

- where to create files
- what each layer is responsible for
- how a request moves through the system

## What We Are Building

We will build a small feature with these ideas:

- a `Project` belongs to a user
- a user can create a project
- a user can list their own projects

This is enough to learn the pattern without adding too much complexity.

## Step 1. Create the Model

Create:

- `app/db/models/project.py`

Your model should usually include:

- `id`
- `name`
- `owner_id`
- timestamps if needed

Use [app/db/models/user.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/db/models/user.py) as a reference.

After that:

1. import the model in `app/db/models/__init__.py`
2. create a migration if your project is already using Alembic in team workflow

## Step 2. Create the Repository

Create:

- `app/db/repositories/project_repository.py`

This file should contain DB operations such as:

- create project
- get project by id
- list projects by owner

Repository rule:

Do not put business validation here.

## Step 3. Create the Schemas

Create:

- `app/schemas/project.py`

You usually need:

- create request schema
- response schema

Example structure:

- `ProjectCreateRequest`
- `ProjectResponse`

Schemas validate input and define API output shape.

## Step 4. Create the Service

Create:

- `app/services/project_service.py`

This service should:

- receive the repository
- create projects
- enforce ownership rules
- return domain results

Example responsibilities:

- trim project names
- reject duplicate names for the same user
- ensure only the owner can access the project

## Step 5. Create the API Route

Create:

- `app/api/v1/projects.py`

Add routes such as:

- `POST /api/v1/projects`
- `GET /api/v1/projects`

Use `get_current_user` so the route is protected.

The route should:

1. read the request body
2. get the current user
3. call the service
4. return the response

## Step 6. Register the Router

Open:

- [app/main.py](/home/iqbal-ai/Downloads/industry_ai_backend_template/app/main.py)

Import the new router and include it.

If you forget this step, your endpoints will not appear.

## Step 7. Add Tests

Create:

- `tests/test_projects.py`

Minimum tests:

- authenticated user can create a project
- authenticated user can list their own projects
- unauthenticated user is rejected

This is enough for the first version.

## Request Flow You Should Understand

When a user sends a request:

1. FastAPI route receives it
2. auth dependency validates the user
3. route calls the service
4. service calls the repository
5. repository reads or writes the database
6. response is returned

This is the basic flow you should repeat for most product features.

## Common Mistakes During First Feature Work

Avoid these:

- writing raw SQL in the route
- putting all logic in the repository
- skipping schemas
- forgetting auth dependency
- forgetting tests

## What To Read Next

After building your first feature, read:

- [docs/USER_GUIDE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/USER_GUIDE.md)
- [docs/ARCHITECTURE.md](/home/iqbal-ai/Downloads/industry_ai_backend_template/docs/ARCHITECTURE.md)

Then build a second feature with the same pattern until the structure feels natural.
