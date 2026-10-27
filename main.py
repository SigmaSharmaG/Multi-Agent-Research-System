# from src.tools.tools import web_search,scrape_url

# # output = web_search("Latest news on AI research")
# # print(output)

# # result = web_search("https://ai.google/research")
# # print(result)

# r = web_search.invoke("What is the latest research on AI")
# print(r)


from src.pipelines.pipeline import run_research_pipeline

topic = "The impact of AI on the job market in 2026"
run_research_pipeline(topic)