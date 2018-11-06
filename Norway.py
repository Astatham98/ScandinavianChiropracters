import requests
import bs4 as bs
import csv


with open('persons.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Name', 'Url', 'Address', 'Number', 'Email'])
csvfile.close()

parsed = 0
l = ['http://www.kiropraktiskaforeningen.se/ort/blekinge-lan/', 'http://www.kiropraktiskaforeningen.se/ort/dalarnas-lan/',
     'http://www.kiropraktiskaforeningen.se/ort/gotlands-lan/', 'http://www.kiropraktiskaforeningen.se/ort/gavleborgs-lan/',
     'http://www.kiropraktiskaforeningen.se/ort/hallands-lan/', 'http://www.kiropraktiskaforeningen.se/ort/jamtlands-lan/',
     'http://www.kiropraktiskaforeningen.se/ort/kalmar-lan/', 'http://www.kiropraktiskaforeningen.se/ort/kronobergs-lan/',
     'http://www.kiropraktiskaforeningen.se/ort/norrbottens-lan/', 'http://www.kiropraktiskaforeningen.se/ort/skane-lan/',
     'http://www.kiropraktiskaforeningen.se/ort/stockholms-lan/', 'http://www.kiropraktiskaforeningen.se/ort/sodermanlands-lan/',
     'http://www.kiropraktiskaforeningen.se/ort/uppsala-lan/', 'http://www.kiropraktiskaforeningen.se/ort/varmlands-lan/',
     'http://www.kiropraktiskaforeningen.se/ort/vasterbottens-lan/', 'http://www.kiropraktiskaforeningen.se/ort/vasternorrlands-lan/',
     'http://www.kiropraktiskaforeningen.se/ort/vastmanlands-lan/', 'http://www.kiropraktiskaforeningen.se/ort/vastra-gotalands-lan/',
     'http://www.kiropraktiskaforeningen.se/ort/orebro-lan/', 'http://www.kiropraktiskaforeningen.se/ort/ostergotlands-lan/']

for a in l:
    url = a
    response = requests.get(url)
    page_content = bs.BeautifulSoup(response.content, 'lxml')
    find = page_content.find_all("a", rel="bookmark")

    # gets links on a regions webpage
    link_list = []
    num = 0
    if num <= len(find):
        for i in find:
            link = find[num]
            url = link['href']
            link_list.append(url)
            num += 1

    test = []
    name_list2 = []
    name_list = []
    company_list = []
    stripped = []
    mail_list = []
    phone_list = []
    address_list = []
    list2 = []
    for i in range(0, len(find)):
        response2 = requests.get(str(link_list[i]))
        page_content2 = bs.BeautifulSoup(response2.content, 'lxml')
        find2 = page_content2.find_all('h1', class_='title')
        find_address = page_content2.find_all(class_="varde")
        find_phone_and_mail = page_content2.find_all('li')
        # for finding names and company
        for j in find2:
            k = j.text.strip()
            o = k.split(',')
            list2.append(o)
        # for finding address
        j = ""
        for r in find_address:
            k = r.text.strip()
            j = j + " " + k
            j = j.replace(',', '.')
        address_list.append(j)

        # For finding phone and mail address
        for x in find_phone_and_mail:
            k = x.text.strip()
            stripped.append(k)
        test.append(len(stripped))


    counterp = 0
    counterm = 0
    for u in range(0, len(stripped)):
        if "Telefon -" in stripped[u]:
            phone = stripped[u]
            phone = phone.strip('Telefon - ')
            phone_list.append(phone)
        elif u == test[counterp]:
            counterp += 1
        elif counterp > len(phone_list):
            phone_list.append('NaN')

        if "E-post" in stripped[u]:
            mail = stripped[u]
            mail = mail.strip('E-post - ')
            mail_list.append(mail)
        elif u == test[counterm]:
            counterm += 1
        elif counterm > len(mail_list):
            mail_list.append('NaN')

    # for splitting name and company
    for i in list2:
        if len(i) > 1:
            name_list.append(i[0])
            company_list.append(i[1])
        else:
            name_list.append(i[0])
            company_list.append('NaN')

    for r in name_list:
        new = r.rstrip()
        name_list2.append(new)

    with open('persons.csv', 'a', newline="") as csvfile:
        filewriter = csv.writer(csvfile)
        for i in range(0, len(link_list)):
            filewriter.writerow([name_list2[i], link_list[i], address_list[i], phone_list[i], mail_list[i]])
        print(len(name_list2), len(link_list), len(address_list), len(phone_list), len(mail_list))
    csvfile.close()
    parsed = parsed + len(name_list2)
    print(parsed)

