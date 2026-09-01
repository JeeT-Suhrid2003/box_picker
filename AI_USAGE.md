# AI Usage Log

## 1. AI tool(s) used

This project was developed with:

- Gemini (for planning and product architecture ideas)
- GitHub Copilot in the VS Code editor (for generating project structure, Django code, API logic, and iterative implementation help)
- Git for branching and separating the manual workflow and Gemini integration work

## 2. Prompts used

### Initial planning prompt

> ok we have a project at hand so first i think we should change the mvp to a better solution by doing 2 projects first a manual input when we are adding a item we add a category to the item corresponding to a list of category of diffrent box types[for now store them in a list], second if we want to automate it we can add agentic pipeline(in our case we will simply use the gemini api ) so when we put a item in for sales, gemini will decide a category to it and a option to manually change it if need be, dont make a interface we will do this in a api calls if we want it to be applied in a microservice system later on like in a cluster it gave me a better written work flow of combining both and having a setback system if api call fails the recommendation system take over and Check dimension fit (L,W,H),Check max payload weight,Filter by category rules, Pick minimum cost box.

### Implementation prompt

> form a project basic environment and do the project in parts first form a recommendation system named manual then add a gemini call and merge both of them

### Git workflow prompt

> use git to separate the development of both projects

## 3. What output was accepted

The following outputs were accepted because they were directly aligned with the MVP and the architecture described in the brief:

- Django project structure creation
- Product and Box models
- manual category override flow
- API routes for products and recommendation
- recommendation engine logic based on size, weight, and category compatibility
- fallback strategy when AI classification fails
- test coverage for product creation and recommendation behavior

The accepted approach was:

- Manual category assignment is used when a category is provided
- Gemini classification fills in the category when it is omitted
- The recommendation system remains deterministic and uses math-based filtering instead of allowing the AI to choose the box
- If the AI call fails, the system falls back to a safe default category instead of crashing

## 4. What output was rejected or modified

The following outputs or assumptions were rejected or fixed during the build:

- The initial Gemini implementation was treated as a placeholder and later replaced with a real API call structure
- Incorrect environment assumptions were corrected, especially around Python/Django setup and environment variables
- Some hallucinated commands and setup steps were discarded because they were not useful or were not actually required in this project
- The initial model name and configuration assumptions were adjusted to a valid Gemini endpoint pattern
- The recommendation logic was validated and corrected when it was too strict for quantity-based orders or mixed category combinations

## 5. Mistakes the AI made

The AI made several mistakes during early iterations:

- It sometimes assumed the environment had already been configured when it had not
- It suggested commands that were not useful for the actual project flow
- It relied on assumptions about environment variables and shell state instead of confirming how they were set in the actual runtime
- It initially treated the API call as a simple placeholder without enough handling for missing keys, timing issues, or invalid responses
- It sometimes hallucinated the project stage or said a step was already done when it had not been fully implemented
- It did not always preserve the distinction between the manual recommendation path and the AI classification path

## 6. How the final code was verified

The final code was verified through a combination of:

- manual terminal testing using PowerShell and Django API calls
- direct inspection of completed endpoints and logic in the project files
- running Django tests for the core behavior
- checking the API contract for product creation, category override, and box recommendation

Verification command used:

```powershell
cd C:\Users\suhri\Documents\coding\box_picker
$env:DJANGO_SETTINGS_MODULE='box_picker_project.settings'
python -m django test core --verbosity 2
```

This was used after the main logic was implemented and after the fallback and Gemini integration fixes were added.

The project includes 4 regression tests covering:

- manual category assignment
- automatic category fallback behavior
- Gemini classification path when available
- recommendation engine selecting the cheapest valid box

These tests were added to validate the final implementation before relying on it for further work.
