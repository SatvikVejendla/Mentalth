import twint
# Configure

tags = ["suicide", "end my life", "want to die"]

c = twint.Config()
c.Limit = 20000
c.Store_csv = True
c.Output = "data/data.csv"
c.Lang = "en"

# Run
for i in tags:
    c.Search = i
    twint.run.Search(c)
