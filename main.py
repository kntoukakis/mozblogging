from time import sleep
from mozscape import Mozscape
import csv

client = Mozscape('******', '******')
# Now I can make API calls!

def get_MozscapeData(url_list):

    authorities = client.urlMetrics(
        #['www.example.com',],
        url_list,
        Mozscape.UMCols.pageAuthority | Mozscape.UMCols.equityExternalLinks | Mozscape.UMCols.domainAuthority
        )
    sleep(11)
    return (authorities)


myFile = open('sheet1.csv','r')
reader = csv.reader(myFile)

row_count = sum(1 for row in myFile)
row_count = int(row_count)
print ("row_count in file: ",row_count)

myFile.close()

myFile = open('sheet1.csv','r')
reader = csv.reader(myFile)

outputFile = open('results/Mozscape.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)

outputWriter.writerow(["URL","External Links","Page Authority","Domain Authority"])

batch_urls = []

which_row = 0
for row in reader:
    which_row = which_row +1
    url = row[0] #The URLs are in the 1st column

    if url == "URL":
        pass
    else:
        try:
            if "http://" in url:
                url = url.replace("http://","")
            if "https://" in url:
                url = url.replace("https://", "")


            #making sure that all requests go without a www subdomain
            if "www." in url:
                url = url.replace("www.", "")
            else:
                pass
            """

            # making sure that all requests go with www
            if "www." in url:
                pass
            else:
                url = "www." + url
            """

            batch_urls.append(url)

            if (len(batch_urls) == 10) or (which_row == row_count):

                print ("New batch...")
                print (batch_urls)
                print ("calling Moz...")

                MozDatas = get_MozscapeData(batch_urls)
                print ("Moz Datas...")
                print (MozDatas)

                count = 0
                for data in MozDatas:

                    url = batch_urls[count]
                    external_links = data["ueid"]
                    page_authority = data["upa"]
                    domain_authority = data["pda"]

                    print(url,external_links,page_authority,domain_authority)
                    outputWriter.writerow([url,external_links,page_authority,domain_authority])
                    count += 1

                #initialize new batch
                print ("initializing new batch...")
                batch_urls = []
                sleep(1)



        except:
            outputWriter.writerow([url, "Error", "Error"])
            print('ERROR WITH URL: ', url)

myFile.close()
outputFile.close()