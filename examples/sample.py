from wiker import Wiker

wk = Wiker(lang='uz', first_article_link="Turkiston")

wk.run(scrape_limit=5)
