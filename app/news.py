from newspaper import Article, Config

import json

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
config = Config()
config.browser_user_agent = user_agent


def analyze(url):
    article = Article(url, config=config)
    article.download()
    article.parse()

    title = article.title
    authors = (
        ("By " + ", ".join(article.authors[:-2] + [" and ".join(article.authors[-2:])]))
        if article.authors
        else ""
    )
    publish_date = article.publish_date
    text = article.text

    article.nlp()

    summary = article.summary

    data = {
        "title": title,
        "authors": authors,
        "publish_date": publish_date.strftime("%m/%d/%Y") if publish_date else "",
        "text": text,
        "summary": summary,
    }

    return data


if __name__ == "__main__":
    print(
        analyze(
            "https://www.nytimes.com/2019/10/27/us/politics/isis-leader-al-baghdadi-dead.html"
        )
    )
