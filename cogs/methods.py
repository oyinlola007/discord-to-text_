import cogs.config as config
import cogs.db as db

def embed_to_text(embed):
    embed_dict = embed.to_dict()
    content = ""

    try:
        content += f"{embed_dict['author']['name']}\n\n"
    except:
        pass

    try:
        content += f"{embed_dict['title']}\n\n"
    except:
        pass

    try:
        content += f"{embed_dict['description']}\n\n"
    except:
        pass

    try:
        for field in embed_dict['fields']:
            content += f"{field['name']}: {field['value']}\n"
    except:
        pass

    try:
        content += f"\n{embed_dict['footer']['text']}"
    except:
        pass

    return content