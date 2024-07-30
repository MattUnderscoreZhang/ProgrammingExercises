import outlines


# TODO: have to use pip instead of pdm or else you get a "pkg_resources" error
# TODO: also have to set OPENAI_API_KEY environment variable in shell


model = outlines.models.openai("gpt-4")
generator = outlines.generate.text(model)
result = generator("What's 2+2?", max_tokens=100)
print(result)
