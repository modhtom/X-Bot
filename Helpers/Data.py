def split_long_sentence(sentence):
    max_length = 275
    sentence = sentence.strip()

    if len(sentence) <= max_length:
        return [sentence]

    chunks = []
    while len(sentence) > max_length:
        last_space = sentence.rfind(" ", 0, max_length)

        if last_space == -1 or last_space < max_length - 20:
            last_space = max_length

        chunks.append(sentence[:last_space].strip())
        sentence = sentence[last_space:].strip()

    if sentence:
        chunks.append(sentence)

    return chunks