city = 'oslo'
with open('static/txt/cities.txt', encoding='utf-8') as file:
    text_and_picture = file.read().replace('\n', '').split('***')
    cities = ['pekin', 'tokyo', 'gonkong', 'paris', 'newyork', 'singapur', 'oslo']
    texts_and_pictures = [i.split('*') for i in text_and_picture]
    for i in range(len(cities)):
        if city == cities[i]:
            print(texts_and_pictures[i])
            text = texts_and_pictures[i][0]
            img = texts_and_pictures[i][1]
            print(text)
            print(img)




