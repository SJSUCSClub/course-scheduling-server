def format_tags(tags):
    # Convert tags list to string
    tags = str(tags)
    tags = tags.replace("[","{").replace("]","}").replace("'","\"")
    return tags