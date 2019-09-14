import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html
from time import sleep
from random import randint
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
import datetime

def removeNonAscii(s):
    return "".join(filter(lambda x: ord(x)<128, s))

def clean_text(input_given):
    input_given = removeNonAscii(input_given)
    input_given = str(input_given)
    input_given = input_given.replace("\n"," ").replace("\t"," ")
    return input_given

def multiple_space_remover(input_given):
    if type(input_given) == str:
        input_given = input_given.strip()
        input_given = clean_text(input_given)
        while("  " in input_given):
            input_given = input_given.replace("  "," ")
        input_given = input_given.strip()

        return input_given
    if type(input_given) == list:
        temp_list = []
        for il in range(0,len(input_given)):
            input_given[il] = input_given[il].strip()
            while("  " in input_given[il]):
                input_given[il] = input_given[il].replace("  "," ")
            input_given[il] = input_given[il].strip()
            input_given[il] = clean_text(input_given[il])
            if len(input_given[il]) > 0:
                temp_list.append(input_given[il])
        return temp_list

def master_category_script():
    def amazon_category_script(input_url):

        def category_finder(input_given):
            if type(input_given) == list:
                for i in range(0,len(input_given)):
                    if input_given[i] == 'Amazon Bestsellers Rank:':
                        temp = input_given[i+1]
                        break

                temp = multiple_space_remover(temp)
                temp = temp.replace(" (","")
                temp = temp.split(" ")
                final = []
                for i in range(0,len(temp)):
                    if temp[i] == "in":
                        start = i
                        break

                final = temp[start+1:]
                final = " ".join(final)
                return final

        
        print("Amazon category script started\n")
        amazon_category_data = []

        try:
            driver.get(input_url)
            sleep(randint(15,20))

            page_no = 1
            next_page_count = 1

            while(next_page_count == 1):
                HTMLTree = html.fromstring(driver.page_source)
                review_hits =  HTMLTree.xpath('//ol[@id="zg-ordered-list"]/li[@class="zg-item-immersion"]')
                for i in range(1, len(review_hits)+1):
                    print("        Page No :",page_no,",", "Product Rank :", i)
                    row_data = []
                    unique_id = str(page_no)+"_"+str(i)
                    row_data.append(unique_id)

                    HTMLTree = html.fromstring(driver.page_source)

                    rank_num = HTMLTree.xpath('//ol[@id="zg-ordered-list"]\
                                                //li[@class="zg-item-immersion"]['+str(i)+']\
                                                //div[@class="a-row a-spacing-none aok-inline-block"]//text()')
                    rank_num = rank_num[0].replace("#","")

                    click_page = driver.find_element_by_xpath('//ol[@id="zg-ordered-list"]\
                                                                //li[@class="zg-item-immersion"]['+str(i)+']\
                                                                //a[@class="a-link-normal"]['+str(1)+'][@href]')
                    driver.get(click_page.get_attribute("href"))
                    sleep(randint(6,8))

                    HTMLTree_1 = html.fromstring(driver.page_source)

                    
                    try:
                        title = HTMLTree_1.xpath('//div[@id="titleSection"]\
                                                    //h1[@id="title"]\
                                                    //span[@id="productTitle"]//text()')
                        title = (multiple_space_remover(title))
                        row_data.append(title[0])
                    except:
                        row_data.append(" ")


                    try:
                        company = HTMLTree_1.xpath('//div[@id="bylineInfo_feature_div"]//text()')
                        company = (multiple_space_remover(company))
                        row_data.append(company[0])
                    except:
                        row_data.append(" ")


                    try:
                        reviews = HTMLTree_1.xpath('//div[@id="averageCustomerReviews"]\
                                                    //span[@id="acrCustomerReviewText"]//text()')
                        reviews = (multiple_space_remover(reviews))
                        reviews = reviews[0].replace("customer reviews","")
                        reviews = reviews.strip()
                        row_data.append(reviews)
                    except:
                        row_data.append(" ")


                    try:
                        stars = HTMLTree_1.xpath('//div[@id="averageCustomerReviews"]\
                                                    //span[@class="a-declarative"][1]//text()')
                        stars = (multiple_space_remover(stars))
                        stars = stars[0].replace("out of 5 stars","")
                        stars = stars.strip()
                        row_data.append(stars)
                    except:
                        row_data.append(" ")

                    row_data.append(rank_num)

                    try:
                        category = HTMLTree_1.xpath('//div[@id="detail_bullets_id"]\
                                                    //div[@class="content"]\
                                                    //li[@id="SalesRank"]//text()')
                        category = (multiple_space_remover(category))
                        category = category_finder(category)
                        row_data.append(category)
                    except:
                        row_data.append(" ")

                    try:
                        sub_cat_rank = HTMLTree_1.xpath('//div[@id="detail_bullets_id"]\
                                                    //div[@class="content"]\
                                                    //li[@id="SalesRank"]\
                                                    //ul[@class="zg_hrsr"]\
                                                    //span[@class="zg_hrsr_rank"]//text()')
                        sub_cat_rank = (multiple_space_remover(sub_cat_rank))
                        sub_cat_rank = sub_cat_rank[0].replace("#","")
                        row_data.append(sub_cat_rank)
                    except:
                        row_data.append(" ")


                    try:
                        sub_cat_name = HTMLTree_1.xpath('//div[@id="detail_bullets_id"]\
                                                    //div[@class="content"]\
                                                    //li[@id="SalesRank"]\
                                                    //ul[@class="zg_hrsr"]\
                                                    //span[@class="zg_hrsr_ladder"]//a//text()')
                        sub_cat_name = (multiple_space_remover(sub_cat_name))
                        row_data.append(sub_cat_name[0])
                    except:
                        row_data.append(" ")

                    try:
                        description = HTMLTree_1.xpath('//div[@id="descriptionAndDetails"]\
                                                        //div[@id="productDescription"]//p//text()')
                        description = (multiple_space_remover(description))
                        row_data.append(description[0])
                    except:
                        row_data.append(" ")
                        
                    try:
                        buy_offers = HTMLTree_1.xpath('//div[@id="shipsFromSoldBy_feature_div"]\
                                                        //div[@id="merchant-info"]\
                                                        //a[@id="sellerProfileTriggerId"]//text()')
                        buy_offers = (multiple_space_remover(buy_offers))
                        row_data.append(buy_offers[0])
                    except:
                        row_data.append(" ")

                    try:
                        total_reviews_link = driver.find_element_by_xpath('//*[@id="reviews-medley-footer"]/div/a')
                        total_reviews_link = (total_reviews_link.get_attribute("href"))
                    except:
                        total_reviews_link = "No link found"

                    try:
                        buy_offers_2 = driver.find_element_by_xpath('//div[@id="moreBuyingChoices_feature_div"]\
                                                        //div[@class="a-box"]\
                                                        //span[@id="mbc-olp-link"]//a')
                        buy_offers_2.click()

                        sleep(randint(6,8))

                        HTMLTree_2 = html.fromstring(driver.page_source)

                        buyers_list =  HTMLTree_2.xpath('//div[@aria-label="More buying choices"]/div[@class="a-row a-spacing-mini olpOffer"]')

                        buyer_list = []

                        for bl in range(1,len(buyers_list)+1):
                            temp_buyer = HTMLTree_2.xpath('//div[@aria-label="More buying choices"]\
                                                        //div[@class="a-row a-spacing-mini olpOffer"]['+str(bl)+']\
                                                        //div[@class="a-column a-span2 olpSellerColumn"]\
                                                        //h3[@class="a-spacing-none olpSellerName"]//text()')

                            temp_buyer = multiple_space_remover(temp_buyer)
                            buyer_list.append(temp_buyer[0])
                        
                        driver.back()
                        sleep(randint(6,8))
                        buyer_list = " | ".join(buyer_list)
                        row_data.append(buyer_list)
                    except:
                        row_data.append("No Extra Buyers")

                    row_data.append(total_reviews_link)

                    driver.back()
                    sleep(randint(6,8))
                    amazon_category_data.append(row_data)

                    break
                    
                try:
                    next_page_link = driver.find_element_by_xpath('//ul[@class="a-pagination"]\
                                                                    //li[@class="a-last"]//a')
                    next_page_link.click()
                    sleep(randint(6,8))
                    page_no = page_no+1
                except:
                    next_page_count = 0

            print("\nAmazon category script Completed")
            return amazon_category_data

        except Exception as e:
            print("Amazon : Unexpected error occured")
            print("         So, comming out of amazon")
            print("         Script will return data, till it encountered error")
        finally:
            return amazon_category_data
        

    def fliipkart_category_script(input_url):
        print("\n\n\nFlipkart category script started\n")
        flipkart_category_data = []

        try:
            total_review_count = 0
            driver.get(input_url)
            sleep(randint(15,20))

            page_no = 1
            next_page_count = 1
            rank = 0

            ##//*[@id="container"]/div/div/div/div/div/div/div/div/div/div/a[starts-with(@class,"_2mylT6")]

            while(next_page_count == 1):
                HTMLTree = html.fromstring(driver.page_source)

                review_hits = driver.find_elements_by_xpath('//a[starts-with(@class,"_2mylT6")]')

                if len(review_hits) == 0:
                    review_hits = driver.find_elements_by_xpath('//a[starts-with(@class,"_31qSD5")]')

                links = []
                for elem in review_hits:
                    links.append(elem.get_attribute("href"))


                for i in range(0, len(links)):
                    total_review_count = total_review_count + 1
                    rank = rank + 1
                    print("        Page No :",page_no ,",", "Product Rank :", i+1)
                    row_data = []
                    unique_id = str(page_no)+"_"+str(i)
                    row_data.append(unique_id)

                    HTMLTree = html.fromstring(driver.page_source)

                    driver.get(links[i])
                    sleep(randint(6,8))

                    HTMLTree_1 = html.fromstring(driver.page_source)
                    
                    try:
                        title = HTMLTree_1.xpath('//div[@class="bhgxx2 col-12-12"]\
                                                    //span[@class="_35KyD6"]//text()')
                        title = (multiple_space_remover(title))
                        row_data.append(title[0])
                    except:
                        row_data.append(" ")

                    company = (title[0].split(" "))[0]
                    row_data.append(company)

                    try:
                        reviews = HTMLTree_1.xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[3]//text()')
                        reviews = (multiple_space_remover(reviews))
                        reviews = reviews[0].replace("Reviews","")
                        reviews = reviews.strip()
                        row_data.append(reviews)
                    except:
                        row_data.append(" ")


                    try:
                        stars = HTMLTree_1.xpath('//*[@class="_2_KrJI"]/div//text()')
                        stars = (stars[0]).strip()
                        row_data.append(stars)
                    except:
                        row_data.append(" ")

                    row_data.append(rank)

                    try:
                        category = HTMLTree_1.xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div//text()')
                        category = (multiple_space_remover(category))
                        row_data.append(" | ".join(category))
                    except:
                        row_data.append(" ")

                    try:
                        sub_cat_rank = HTMLTree_1.xpath('//div[@id="detail_bullets_id"]\
                                                    //div[@class="content"]\
                                                    //li[@id="SalesRank"]\
                                                    //ul[@class="zg_hrsr"]\
                                                    //span[@class="zg_hrsr_rank"]//text()')
                        sub_cat_rank = (multiple_space_remover(sub_cat_rank))
                        sub_cat_rank = sub_cat_rank[0].replace("#","")
                        row_data.append(sub_cat_rank)
                    except:
                        row_data.append("No data Found")


                    try:
                        sub_cat_name = HTMLTree_1.xpath('//div[@id="detail_bullets_id"]\
                                                    //div[@class="content"]\
                                                    //li[@id="SalesRank"]\
                                                    //ul[@class="zg_hrsr"]\
                                                    //span[@class="zg_hrsr_ladder"]//a//text()')
                        sub_cat_name = (multiple_space_remover(sub_cat_name))
                        row_data.append(sub_cat_name[0])
                    except:
                        row_data.append("No data Found")

                    try:
                        description = HTMLTree_1.xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[8]/div[4]/div/div[2]/div[1]//text()')
                        description = (multiple_space_remover(description))
                        row_data.append(" | ".join(description))
                    except:
                        row_data.append(" ")
                        
                    try:
                        seller_name = HTMLTree_1.xpath('//*[@id="sellerName"]/span/span//text()')
                        seller_name = (multiple_space_remover(seller_name))
                        row_data.append(seller_name[0])
                    except:
                        row_data.append("No data Found")

                    try:
                        total_reviews_link = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[8]/div/div/a')
                        total_reviews_link = (total_reviews_link.get_attribute("href"))
                    except:
                        total_reviews_link = "No link found"

                    if total_reviews_link == "No link found":
                        try:
                            total_reviews_link = driver.find_element_by_xpath('//*[@id="container"]/div/div/div/div/div/div/div/div/a')
                            total_reviews_link = (total_reviews_link.get_attribute("href"))
                        except:
                            total_reviews_link = "No link found"
                        
                    
                    try:
                        buy_offers_2 = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[8]/div[2]/div/div[2]//li/a')
                        driver.get(buy_offers_2.get_attribute("href"))

                        sleep(randint(6,8))

                        HTMLTree_2 = html.fromstring(driver.page_source)

                        buyers_list =  HTMLTree_2.xpath('//div[@class="_2VDj-t"]/div[@class="_3pZJne"]')

                        total_buyers_list = []

                        for bl in range(1,len(buyers_list)+1):
                            temp_list = []
                            temp_buyer_name = HTMLTree_2.xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[2]/div['+str(bl)+']/div[1]/div[1]/span//text()')
                            temp_buyer_name = multiple_space_remover(temp_buyer_name)
                            temp_list.append(temp_buyer_name[0])

                            total_buyers_list.append(temp_list[0])
                        
                        driver.back()
                        sleep(randint(6,8))
                        row_data.append(" | ".join(total_buyers_list))
                    except:
                        row_data.append("No Extra Buyers")
                    
                    row_data.append(total_reviews_link)
                    driver.back()
                    sleep(randint(6,8))
                    flipkart_category_data.append(row_data)

                    if total_review_count == 10:
                        break
                    
                try:
                    next_page_link = driver.find_elements_by_xpath('//nav[@class="_1ypTlJ"]\
                                                                    //a[@class="_3fVaIS"]')
                    next_page_links = []
                    for npl in next_page_link:
                        next_page_links.append(npl.get_attribute("href"))

                    driver.get(next_page_links[-1])
                    sleep(randint(6,8))
                    page_no = page_no+1
                except Exception as e:
                    print("Flipkart : came to exception in next page link ")
                    next_page_count = 0

                if total_review_count == 10:
                    break

            print("\nFlipkart category script completed")
            return flipkart_category_data

        except Exception as e:
            print(str(e))
            print("Flipkart : Unexpected error occured")
            print("           So, comming out of amazon")
            print("           Script will return data, till it encountered error")
        finally:
            return flipkart_category_data


    driver = webdriver.Firefox()
    datain = csv.reader(open("master_category_script_input_sheet.csv","r"))
    dataout = open("master_category_script_input_sheet_results.csv","w", newline='')
    datawrite = csv.writer(dataout)

    header = ["Website","Review ID", "Product_Title", "Product_Company", \
              "Product_reviews", "Product_ratings", "Product_Bestseller_rank", \
              "Product_category", "Product_Bestseller_subrank", "Product_subcategory", \
              "Product_description", "Product_sold_by", "Other_Buyers", "reviews link"]
    datawrite.writerow(header)

    for index,each in enumerate(datain):
        if index == 0:
            pass
        else:
##            if len(each[0]) > 0 :
##                got_data = amazon_category_script(each[0])
##                for i in range(0,len(got_data)):
##                    data = ["Amazon"] + got_data[i]
##                    datawrite.writerow(data)
            
            if len(each[1]) > 0 :
                got_data = fliipkart_category_script(each[1])
                for i in range(0,len(got_data)):
                    data = ["Flipkart"] + got_data[i]
                    datawrite.writerow(data)
            

    dataout.close()
    driver.close()
    print("Master Category Script Completed")


def master_reviews_script():
    def amazon_script(input_url):
        print("Amazon Reviows Script Started\n")
        amazon_data = []
        try:
            driver.get(input_url)
            sleep(randint(15,20))
            page_no = 1
            to_continue = 1
            total_review_cnt = 0

            while(to_continue == 1):
                HTMLTree = html.fromstring(driver.page_source)
                review_hits =  HTMLTree.xpath('//div[@id="cm_cr-review_list"]/div[@data-hook="review"]')
                print("        Page No :",page_no ,",", "Review Total : ", len(review_hits))
                for i in range(1,len(review_hits)+1):
                    total_review_cnt = total_review_cnt + 1
                    row_data = []
                    unique_id = str(page_no)+"_"+str(i)
                    row_data.append(unique_id)
                    

                    review_title = HTMLTree.xpath('//div[@id="cm_cr-review_list"]\
                                                //div[@data-hook="review"]['+str(i)+']\
                                                //div[@class="a-row"]\
                                                //a[@data-hook="review-title"]\
                                                //span//text()')

                    review_title = multiple_space_remover(review_title)
                    row_data.append((" | ".join(review_title)))

                    #############################################################################

                    review_data = HTMLTree.xpath('//div[@id="cm_cr-review_list"]\
                                            //div[@data-hook="review"]['+str(i)+']\
                                            //div[@class="a-row a-spacing-small review-data"]\
                                            //span[@data-hook="review-body"]//text()')

                    review_data = multiple_space_remover(review_data)
                    row_data.append((" | ".join(review_data)))

                    #############################################################################

                    stars = HTMLTree.xpath('//div[@id="cm_cr-review_list"]\
                                            //div[@data-hook="review"]['+str(i)+']\
                                            //div[@class="a-row"]\
                                            //a[@class="a-link-normal"]\
                                            //span[@class="a-icon-alt"]//text()')
                    if len(stars) > 0:
                        stars = multiple_space_remover(stars)
                        stars = stars[0].replace(".0 out of 5 stars","")
                    else:
                        stars = ""
                    row_data.append(stars)

                    #############################################################################

                    review_date = HTMLTree.xpath('//div[@id="cm_cr-review_list"]\
                                            //div[@data-hook="review"]['+str(i)+']\
                                            //span[@data-hook="review-date"]//text()')

                    review_date = multiple_space_remover(review_date)
                    row_data.append((" | ".join(review_date)))

                    #############################################################################

                    review_views = "No Data Found"
                    row_data.append(review_views)

                    #############################################################################

                    helpful_stmt = HTMLTree.xpath('//div[@id="cm_cr-review_list"]\
                                            //div[@data-hook="review"]['+str(i)+']\
                                            //span[@data-hook="helpful-vote-statement"]//text()')

                    if len(helpful_stmt) > 0:
                        helpful_stmt = multiple_space_remover(helpful_stmt)
                        helpful_stmt = helpful_stmt[0].replace("One person found this helpful","1")
                        helpful_stmt = helpful_stmt[0].replace("people found this helpful","")
                        helpful_stmt = multiple_space_remover(helpful_stmt)
                    else:
                        helpful_stmt = ""
                    row_data.append(helpful_stmt)

                    #############################################################################

                    try:
                        review_purchase_verified = HTMLTree.xpath('//div[@id="cm_cr-review_list"]\
                                                //div[@data-hook="review"]['+str(i)+']\
                                                //span[@class="a-declarative"]\
                                                //span[@data-hook="avp-badge"]//text()')

                        review_purchase_verified = multiple_space_remover(review_purchase_verified)
                        
                    except:
                        review_purchase_verified = ""

                    if len(review_purchase_verified) > 0:
                        review_purchase_verified = 1
                    else:
                        review_purchase_verified = 0
                        
                    row_data.append(review_purchase_verified) 

                    #############################################################################

                    reviews_comments = HTMLTree.xpath('//div[@id="cm_cr-review_list"]\
                                            //div[@data-hook="review"]['+str(i)+']\
                                            //span[@class="a-expander-prompt"]//text()')
                    row_data.append(reviews_comments[0])
                    

                    #############################################################################

                    reviewer_name = HTMLTree.xpath('//div[@id="cm_cr-review_list"]\
                                                //div[@data-hook="review"]['+str(i)+']\
                                                //div[@data-hook="genome-widget"]\
                                                //div[@class="a-profile-content"]\
                                                //span[@class="a-profile-name"]//text()')

                    reviewer_name = multiple_space_remover(reviewer_name)
                    row_data.append((" | ".join(reviewer_name)))

                    #############################################################################

                    try:
                        reviewer_profile = driver.find_element_by_xpath('//div[@id="cm_cr-review_list"]\
                                                    //div[@data-hook="review"]['+str(i)+']\
                                                    //div[@data-hook="genome-widget"]\
                                                    //a[@class="a-profile"]')

                        reviewer_profile.click()
                        sleep(randint(3,5))

                        #############################################################################

                        HTMLTree_1 = html.fromstring(driver.page_source)
                        sleep(1)
                        
                        reviewer_address = HTMLTree_1.xpath('//div[@id="customer-profile-name-header"]\
                                                            //div[@class="a-row a-spacing-base bio-occupation-location"]\
                                                            //text()')
                        if len(reviewer_address) > 0:
                            reviewer_address = reviewer_address[0].split("|")
                            reviewer_address = multiple_space_remover(reviewer_address)
                            if len(reviewer_address) > 1:
                                reviewer_address = reviewer_address[1]
                            else:
                                reviewer_address = reviewer_address[0]
                        else:
                            reviewer_address = "No Data Found"
                            
                        row_data.append(reviewer_address)

                        #############################################################################

                        reviewer_rank = HTMLTree_1.xpath('//div[@class="a-row a-spacing-base"]//text()')

                        
                        if len(reviewer_rank) > 0:
                            reviewer_rank = multiple_space_remover(reviewer_rank)
                            if len(reviewer_rank) > 1:
                                reviewer_rank = reviewer_rank[1].replace("#","")
                            else:
                                reviewer_rank = ""
                        else:
                            reviewer_rank = ""
                        row_data.append(reviewer_rank)

                        #############################################################################

                        reviewer_about = HTMLTree_1.xpath('//span[@class="a-size-base a-color-base read-more-text"]//text()')

                        reviewer_about = multiple_space_remover(reviewer_about)
                        row_data.append(reviewer_about)

                        driver.back()
                    except:
                        row_data.append("No data Found")
                        row_data.append("No data Found")
                        row_data.append("No data Found")

                    #############################################################################

                    amazon_data.append(row_data)

                    sleep(randint(3,5))

                    if total_review_cnt == 5:
                        break

                try:
                    next_page = driver.find_element_by_xpath('//div[@id="cm_cr-pagination_bar"]\
                                                            //li[@class="a-last"]\
                                                            //a')
                    next_page.click()
                    page_no = page_no + 1
                    sleep(randint(10,15))
                    to_continue = 1
                except:
                    print("No Next Page")
                    to_continue = 0

                if total_review_cnt == 5:
                    break

            print("Amazon Script completed")
            return amazon_data
        except Exception as e:
            print(str(e))
            print("Amazon : Unexpected error occured")
            print("         So, comming out of amazon")
            print("         Script will return data, till it encountered error")
        finally:
            return amazon_data

    def flipkart_script(input_url):
        print("\n\nFlipkart Script started\n")
        flipkart_data = []
        try:
            driver.get(input_url)
            sleep(randint(15,20))
            page_no = 1
            to_continue = 1

            total_review_cnt = 0

            while(to_continue == 1):
                HTMLTree = html.fromstring(driver.page_source)
                review_hits =  HTMLTree.xpath('//div[@class="_1HmYoV _35HD7C col-9-12"]/div[@class="bhgxx2 col-12-12"]')
                print("        Page No : ",page_no ,",", "Review Total : ", len(review_hits))
                #len(review_hits)+1
                for i in range(2,len(review_hits)):
                    total_review_cnt = total_review_cnt + 1
                    row_data = []
                    unique_id = str(page_no)+"_"+str(i-1)
                    row_data.append(unique_id)
                    

                    review_title = HTMLTree.xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div[3]/div/div/div/div[1]/p//text()')

                    review_title = multiple_space_remover(review_title)
                    row_data.append((" | ".join(review_title)))

                    #############################################################################

                    try:
                        large_text = driver.find_element_by_xpath('//div[@class="_1HmYoV _35HD7C col-9-12"]\
                                                                    //div[@class="bhgxx2 col-12-12"]['+str(i)+']\
                                                                    //div[@class="_1PBCrt"]//div[@class="col"]\
                                                                    //div[@class="col _390CkK _1gY8H-"]\
                                                                    //div[@class="row"]['+str(2)+']//span[@class="_1EPkIx"]')
                        large_text.click()
                        sleep(randint(3,5))
                    except:
                        pass

                    review_data = HTMLTree.xpath('//div[@class="_1HmYoV _35HD7C col-9-12"]\
                                                    //div[@class="bhgxx2 col-12-12"]['+str(i)+']\
                                                    //div[@class="_1PBCrt"]//div[@class="col"]\
                                                    //div[@class="col _390CkK _1gY8H-"]\
                                                    //div[@class="row"]['+str(2)+']//div[@class="qwjRop"]//text()')

                    review_data = multiple_space_remover(review_data)
                    row_data.append(" | ".join(review_data))

                    #############################################################################

                    stars = HTMLTree.xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div[3]/div/div/div/div[1]/div//text()')
                    
                    stars = multiple_space_remover(stars)
                    row_data.append(stars[0])

                    #############################################################################

                    review_date = HTMLTree.xpath('//div[@class="_1HmYoV _35HD7C col-9-12"]\
                                                    //div[@class="bhgxx2 col-12-12"]['+str(i)+']\
                                                    //div[@class="_1PBCrt"]//div[@class="col"]\
                                                    //div[@class="col _390CkK _1gY8H-"]\
                                                    //div[@class="row _2pclJg"]\
                                                    //div[@class="row"]//p[@class="_3LYOAd"]//text()')

                    review_date = multiple_space_remover(review_date)
                    row_data.append((" | ".join(review_date)))

                    #############################################################################

                    review_views = "No Data Found"
                    row_data.append(review_views)

                    #############################################################################

                    helpful_stmt = HTMLTree.xpath('//div[@class="_1HmYoV _35HD7C col-9-12"]\
                                                    //div[@class="bhgxx2 col-12-12"]['+str(i)+']\
                                                    //div[@class="_1PBCrt"]//div[@class="col"]\
                                                    //div[@class="col _390CkK _1gY8H-"]\
                                                    //div[@class="row _2pclJg"]\
                                                    //div[@class="_3KBEVV"]\
                                                    //div[@class="row"]\
                                                    //div[@class="NIDnsQ"]//div[@class="_2ZibVB"]\
                                                    //span[@class="_1_BQL8"]//text()')

                    helpful_stmt = multiple_space_remover(helpful_stmt)
                    row_data.append(helpful_stmt[0])

                    #############################################################################

                    try:
                        review_purchase_verified = HTMLTree.xpath('//div[@class="_1HmYoV _35HD7C col-9-12"]\
                                                    //div[@class="bhgxx2 col-12-12"]['+str(i)+']\
                                                    //div[@class="_1PBCrt"]//div[@class="col"]\
                                                    //div[@class="col _390CkK _1gY8H-"]\
                                                    //div[@class="row _2pclJg"]\
                                                    //div[@class="row"]//p[@class="_19inI8"]//span['+str(1)+']//text()')

                        review_purchase_verified = multiple_space_remover(review_purchase_verified)
                        
                    except:
                        review_purchase_verified = ""

                    if len(review_purchase_verified) > 0:
                        review_purchase_verified = 1
                    else:
                        review_purchase_verified = 0
                        
                    row_data.append(review_purchase_verified) 

                    #############################################################################

                    reviews_comments = "No Data Found"
                    row_data.append(reviews_comments)

                    #############################################################################

                    reviewer_name = HTMLTree.xpath('//div[@class="_1HmYoV _35HD7C col-9-12"]\
                                                    //div[@class="bhgxx2 col-12-12"]['+str(i)+']\
                                                    //div[@class="_1PBCrt"]//div[@class="col"]\
                                                    //div[@class="col _390CkK _1gY8H-"]\
                                                    //div[@class="row _2pclJg"]\
                                                    //div[@class="row"]//p[@class="_3LYOAd _3sxSiS"]//text()')

                    reviewer_name = multiple_space_remover(reviewer_name)
                    row_data.append((" | ".join(reviewer_name)))

                    #############################################################################
                    
                    reviewer_address = HTMLTree.xpath('//div[@class="_1HmYoV _35HD7C col-9-12"]\
                                                    //div[@class="bhgxx2 col-12-12"]['+str(i)+']\
                                                    //div[@class="_1PBCrt"]//div[@class="col"]\
                                                    //div[@class="col _390CkK _1gY8H-"]\
                                                    //div[@class="row _2pclJg"]\
                                                    //div[@class="row"]//p[@class="_19inI8"]//span['+str(2)+']//text()')
                    
                    reviewer_address = multiple_space_remover(reviewer_address)
                    if len(reviewer_address) > 0:
                        if reviewer_address[0].startswith(", "):
                            reviewer_address[0] = reviewer_address[0][1:]
                            reviewer_address[0] = multiple_space_remover(reviewer_address[0])
                    else:
                        reviewer_address = ["No data found"]
                    row_data.append(reviewer_address[0])

                    #############################################################################

                    reviewer_rank = "No Data Found"
                    row_data.append(reviewer_rank)

                    #############################################################################

                    reviewer_about = "No Data Found"
                    row_data.append(reviewer_about)

                    #############################################################################

                    flipkart_data.append(row_data)

                    sleep(randint(3,5))

                    if total_review_cnt == 5:
                        break

                try:
                    try:
                        next_page = driver.find_element_by_xpath('//div[@class="_2zg3yZ _3KSYCY"]\
                                                                //nav[@class="_1ypTlJ"]\
                                                                //a[@class="_3fVaIS"]['+str(2)+']')
                    except:
                        next_page = driver.find_element_by_xpath('//div[@class="_2zg3yZ _3KSYCY"]\
                                                                //nav[@class="_1ypTlJ"]\
                                                                //a[@class="_3fVaIS"]['+str(1)+']')
                        
                    next_page.click()
                    page_no = page_no + 1
                    sleep(randint(10,15))
                    to_continue = 1
                except:
                    print("No Next Page")
                    to_continue = 0

                if total_review_cnt == 5:
                    break

            print("\n\nFlipkart Script completed")
            return flipkart_data
        except Exception as e:
            print(str(e))
            print("Flipkart : Unexpected error occured")
            print("           So, comming out of amazon")
            print("           Script will return data, till it encountered error")
        finally:
            return flipkart_data
    

    def trust_pilot(input_url):

        def star_finder_trust_pilot(input_given):
            if "5" in input_given:
                return "5"
            elif "4" in input_given:
                return "4"
            elif "3" in input_given:
                return "3"
            elif "2" in input_given:
                return "2"
            elif "1" in input_given:
                return "1"
            else:
                return "Not Found"
        
        print("\n\nTrust Pilot Started\n")
        trust_pilot_data = []

        try:
            driver.get(input_url)
            sleep(randint(15,20))
            page_no = 1
            to_continue = 1

            HTMLTree_1 = html.fromstring(driver.page_source)

            reviews_list =  HTMLTree_1.xpath('//div[@class="review-list"]/div[@class="review-card  "]')

            while (to_continue == 1):
                print("        Page No : ", page_no)
                for hit in range(1,(len(reviews_list)+1)):
                    row_data = []
                    unique_id = str(page_no)+"_"+str(hit)
                    row_data.append(unique_id)

                    HTMLTree = html.fromstring(driver.page_source)

                    review_title = HTMLTree.xpath('//div[@class="review-list"]\
                                                    //div[@class="review-card  "]['+str(hit)+']\
                                                    //section[@class="review__content"]\
                                                    //div[@class="review-content__body"]\
                                                    //h2[@class="review-content__title"]//text()')
                    review_title = multiple_space_remover(review_title)
                    row_data.append(review_title)

                    ###############################################

                    review_text = HTMLTree.xpath('//div[@class="review-list"]\
                                                    //div[@class="review-card  "]['+str(hit)+']\
                                                    //section[@class="review__content"]\
                                                    //div[@class="review-content__body"]\
                                                    //p[@class="review-content__text"]//text()')
                    review_text = multiple_space_remover(review_text)
                    row_data.append(review_text)

                    ###############################################

                    review_stars = HTMLTree.xpath('//div[@class="review-list"]\
                                                    //div[@class="review-card  "]['+str(hit)+']\
                                                    //section[@class="review__content"]\
                                                    //div[@class="review-content__header"]\
                                                    //div[@class="review-content-header"]//@class')
                    review_stars = multiple_space_remover(str(review_stars[1]))
                    review_stars = star_finder_trust_pilot(review_stars)
                    row_data.append(review_stars)

                    #############################################################################

                    review_date = HTMLTree.xpath('//div[@class="review-list"]\
                                                    //div[@class="review-card  "]['+str(hit)+']\
                                                    //section[@class="review__content"]\
                                                    //div[@class="review-content-header"]\
                                                    //div[@class="review-content-header__dates"]\
                                                    //div[@class="v-popover"]//time//text()')
                    review_date = multiple_space_remover(review_date)
                    row_data.append(review_date)

                    #############################################

                    review_views = "No Data Found"
                    row_data.append(review_views)

                    ###############################################

                    review_helpful = "No Data Found"
                    row_data.append(review_helpful)

                    ###############################################

                    try:
                        review_purchase_verified = HTMLTree.xpath('//div[@class="review-list"]\
                                                    //div[@class="review-card  "]['+str(hit)+']\
                                                    //section[@class="review__content"]\
                                                    //div[@class="review-content__header"]\
                                                    //div[@class="review-content-header__review-verified"]//text()')

                        review_purchase_verified = multiple_space_remover(review_purchase_verified)
                            
                    except:
                        review_purchase_verified = ""

                    if len(review_purchase_verified) > 0:
                        review_purchase_verified = 1
                    else:
                        review_purchase_verified = 0
                        
                    row_data.append(review_purchase_verified) 

                    #############################################################################

                    reviews_comments = "No Data Found"
                    row_data.append(reviews_comments)

                    #############################################################################
                    
                    review_name = HTMLTree.xpath('//div[@class="review-list"]\
                                                    //div[@class="review-card  "]['+str(hit)+']\
                                                    //aside[@class="review__consumer-information"]\
                                                    //div[@class="consumer-information__name"]//text()')
                    review_name = multiple_space_remover(review_name)
                    row_data.append(review_name)

                    #############################################################################

                    reviewer_address = "No Data Found"
                    row_data.append(reviewer_address)

                    #############################################################################

                    reviewer_rank = "No Data Found"
                    row_data.append(reviewer_rank)

                    #############################################################################

                    reviewer_about = "No Data Found"
                    row_data.append(reviewer_about)
                    
                    trust_pilot_data.append(row_data)
                    
                try:
                    next_page = driver.find_element_by_xpath('//nav[@rel="nav"]\
                                                            //a[@class="button button--primary next-page"][@href]')
                    next_page = next_page.get_attribute("href")
                    driver.get(next_page)
                    sleep(randint(8,12))
                    page_no = page_no + 1
                    to_continue = 1
                except:
                    print("No Next Page")
                    to_continue = 0

            print("\n\nTrust Pilot Script completed")
            return trust_pilot_data

        finally:
            print("Trust Pilot : Unexpected error occured")
            print("              So, comming out of amazon")
            print("              Script will return data, till it encountered error")
            return trust_pilot_data
            


    def mouthshut(input_url):
        print("\n\nMouth Shut Started\n")
        def star_finder_mouthshut(input_given):
            temp_list = []
            count = 0
            for i in range(0,len(input_given)):
                if input_given[i] == "icon-rating rated-star":
                    count = count + 1
            return count

        mouthshut_data = []
        try:
            driver.get(input_url)
            sleep(randint(15,20))
            
            try:
                not_now = driver.find_element_by_xpath('//div[@class="popupFooterText"]//a[@id="notifynotnow"]')
                not_now.click()
                sleep(5)
            except:
                pass

            page_no = 1
            to_continue = 1

            while(to_continue == 1):
                print("        Page No : ", page_no)
                HTMLTree = html.fromstring(driver.page_source)
                reviews_list =  HTMLTree.xpath('//div[@id="dvreview-listing"]/div[@class="row review-article"]')
                for hit in range(1,(len(reviews_list))+1):
                    row_data = []
                    unique_id = str(page_no)+"_"+str(hit)
                    row_data.append(unique_id)

                    element_to_hover_over_2 = driver.find_element_by_xpath('//div[@id="dvreview-listing"]\
                                                                //div[@class="row review-article"]['+str(hit)+']\
                                                                //div[@class="more reviewdata"]//a')
                    element_to_hover_over_2.click()
                    sleep(randint(3,5))

                    HTMLTree_1 = html.fromstring(driver.page_source)

                    #######################################################################################

                    review_title = HTMLTree_1.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl00_lnkTitle"]//text()')

                    review_title = multiple_space_remover(review_title)
                    row_data.append(review_title)

                    #######################################################################################

                    review_text = HTMLTree_1.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl00_lireviewdetails"]/div[3]/p//text()')

                    review_text = multiple_space_remover(review_text)
                    row_data.append(review_text)

                    #######################################################################################

                    review_stars = HTMLTree_1.xpath('//div[@id="dvreview-listing"]\
                                                    //div[@class="row review-article"]['+str(hit)+']\
                                                    //div[@class="rating"]//@class')

                    review_stars = multiple_space_remover(review_stars)
                    review_stars = star_finder_mouthshut(review_stars)
                    row_data.append(review_stars)

                    #######################################################################################

                    review_date = HTMLTree_1.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl00_smdatetime"]//text()')
                    review_date = multiple_space_remover(review_date)
                    row_data.append(review_date)

                    #######################################################################################

                    review_views = HTMLTree_1.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl00_lireviewdetails"]/div[2]/span[3]//text()')
                    review_views = multiple_space_remover(review_views)
                    row_data.append(review_views)

                    #######################################################################################

                    review_helpful = "No Data Found"
                    row_data.append(review_helpful)

                    #######################################################################################

                    review_purchase_verified = "No Data Found"
                    row_data.append(review_purchase_verified)

                    #######################################################################################

                    reviews_comments = HTMLTree_1.xpath('//div[@id="dvreview-listing"]\
                                                        //div[@class="row review-article"]['+str(hit)+']\
                                                        //div[@class="count-section"]\
                                                        //div[@class="comment-clk"]//a//span//text()')
                    reviews_comments = reviews_comments[0].replace("Comments","").replace("(","").replace(")","")
                    reviews_comments = multiple_space_remover(reviews_comments)
                    row_data.append(reviews_comments)

                    ######################################################################################

                    reviewer_name = HTMLTree_1.xpath('//div[@id="dvreview-listing"]\
                                                        //div[@class="row review-article"]['+str(hit)+']\
                                                        //div[@class="user-ms-name"]//a//text()')

                    reviewer_name = multiple_space_remover(reviewer_name)
                    row_data.append(reviewer_name)

                    ######################################################################################

                    reviewer_address = HTMLTree_1.xpath('//div[@id="dvreview-listing"]\
                                                        //div[@class="row review-article"]['+str(hit)+']\
                                                        //div[@class="usr-addr-text"]//text()')

                    reviewer_address = multiple_space_remover(reviewer_address)
                    row_data.append(reviewer_address)

                    ######################################################################################

                    reviewer_rank = "No Data Found"
                    row_data.append(reviewer_rank)

                    #######################################################################################

                    reviewer_about = "No Data Found"
                    row_data.append(reviewer_about)
                    
                    mouthshut_data.append(row_data)
                    sleep(randint(3,5))
                
                try:
                    next_link = driver.find_element_by_xpath('//ul[@class="pagination table"]\
                                                        //li[@class="next"]//a[@class="btn btn-link"][@href]')
                    next_link = next_link.get_attribute("href")
                    driver.get(next_link)
                    sleep(randint(7,10))
                    page_no = page_no + 1
                    to_continue = 1
                except:
                    print("No Next Page")
                    to_continue = 0

            print("\n\nMouth Shut Script completed")
            return mouthshut_data

        finally:
            print("Mouth Shut : Unexpected error occured")
            print("             So, comming out of amazon")
            print("             Script will return data, till it encountered error")
            return mouthshut_data
            


    def google_play_store(input_url):
        def star_finder_google_play_store(input_given):
            if "5" in input_given:
                return "5"
            elif "4" in input_given:
                return "4"
            elif "3" in input_given:
                return "3"
            elif "2" in input_given:
                return "2"
            elif "1" in input_given:
                return "1"
            else:
                return "Not Found"

        print("\n\nGoogle play Store Started\n")
        google_play_store_data = []

        try:
            driver.get(input_url)
            sleep(randint(15,20))

            page_no = 1

            HTMLTree = html.fromstring(driver.page_source)
            review_hits =  HTMLTree.xpath('//span[@class="AYi5wd TBRnV"]//text()')

            total_reviews = int(review_hits[0].replace(",",""))

            i = 1

            while(i < total_reviews + 1):
                if (i % 20) == 0:
                    print("        {} completed out of {}".format(i,total_reviews))
                    driver.find_element_by_tag_name('body').send_keys(Keys.END) 
                    sleep(randint(4,6))

                    try:
                        more_box = driver.find_element_by_xpath('//div[@class="PFAhAf"]\
                                                        //span[@class="RveJvd snByac"]')
                        more_box.click()
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        sleep(randint(3,5))
                    except:
                        pass

                try:
                    expand = driver.find_element_by_xpath('//div[@jsname="fk8dgd"]\
                                                //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                                //div[@class="UD7Dzf"]\
                                                //div[@class="cQj82c"]\
                                                //button[@class="LkLjZd ScJHi OzU4dc  "]')
                    expand.click()
                    sleep(randint(3,5))
                except:
                    pass
                    
                HTMLTree = html.fromstring(driver.page_source)
                row_data = []
                row_data.append(i)

                ##############################################################

                review_title = "No Data Found"
                row_data.append(review_title)

                ##############################################################

                review_text = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                                //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                                //div[@class="UD7Dzf"]\
                                                //span[@jsname="fbQN7e"]//text()')

                review_text = multiple_space_remover(review_text)
                row_data.append((" | ".join(review_text)))

                ###############################################################

                review_stars = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                                //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                                //div[@class="bAhLNe kx8XBd"]\
                                                //span[@class="nt2C1d"]\
                                                //div[@class="pf5lIe"]//div//@aria-label')

                review_stars = multiple_space_remover(str(review_stars[0]))
                review_stars = star_finder_mouth_shut(review_stars)
                row_data.append((" | ".join(review_stars)))

                ###############################################################

                review_date = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                                //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                                //div[@class="bAhLNe kx8XBd"]\
                                                //span[@class="p2TkOb"]//text()')

                review_date = multiple_space_remover(review_date)
                row_data.append((" | ".join(review_date)))

                ###############################################################

                review_views = "No Data Found"
                row_data.append(review_views)

                ###############################################################

                helpful_stmt = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                                //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                                //div[@class="YCMBp GVFJbb"]\
                                                //div[@class="jUL89d y92BAb"]//text()')

                helpful_stmt = multiple_space_remover(helpful_stmt)
                row_data.append((" | ".join(helpful_stmt)))

                ###############################################################

                review_verified = "No Data Found"
                row_data.append(review_verified)

                ###############################################################

                review_comments = "No Data Found"
                row_data.append(review_comments)

                ###############################################################
                        
                reviewer_name = HTMLTree.xpath('//div[@jsname="fk8dgd"]\
                                                //div[@jsmodel="y8Aajc"]['+str(i)+']\
                                                //div[@class="bAhLNe kx8XBd"]\
                                                //span[@class="X43Kjb"]//text()')

                reviewer_name = multiple_space_remover(reviewer_name)
                row_data.append((" | ".join(reviewer_name)))

                ###############################################################

                reviewer_address = "No Data Found"
                row_data.append(reviewer_address)

                ###############################################################

                reviewer_rank = "No Data Found"
                row_data.append(reviewer_rank)

                ###############################################################

                reviewer_about = "No Data Found"
                row_data.append(reviewer_about)

                google_play_store_data.append(row_data)
                i = i + 1

            print("\n\nGoogle Play store Script completed")
            return google_play_store_data
        finally:
            print("Google play store : Unexpected error occured")
            print("                    So, comming out of amazon")
            print("                    Script will return data, till it encountered error")
            return google_play_store_data

    driver = webdriver.Firefox()
    datain = csv.reader(open("master_category_script_input_sheet_results.csv","r"))
    header = ["Website","Review ID", "Review_Title", "Review_Text", \
              "Review_Stars", "Review_Date", "Review_Views", \
              "Review_helpful", "Review_Verified", "Number_of_comments", \
              "Reviewer_Name", "Reviewer_Address", "Reviewer_Rank",\
              "Reviewer_About"]

    for index,each in enumerate(datain):
        if index == 0:
            pass
        else:
            if len(each[13]) > 0 and each[13]!= "No link found":
                file_name = each[0]+"_"+each[1]+"_"+each[2]
                dataout = open(file_name+"_reviews.csv","w", newline='')
                datawrite = csv.writer(dataout)
                datawrite.writerow(header)
                if each[0] == "Amazon":
                    got_data = amazon_script(each[13])
                    for i in range(0,len(got_data)):
                        data = ["Amazon"] + got_data[i]
                        datawrite.writerow(data)

                if each[0] == "Flipkart":
                    got_data = flipkart_script(each[13])
                    for i in range(0,len(got_data)):
                        data = ["Flipkart"] + got_data[i]
                        datawrite.writerow(data)

                dataout.close()
    driver.close()
    print("Master reviews crawler completed")

master_category_script()
#master_reviews_script()
