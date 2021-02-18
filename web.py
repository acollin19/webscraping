
import requests, bs4
import matplotlib.pyplot as plt
import pickle 

#Web scraping: Get the website and raise for status. Use soup and selct to pick the piece on the website I want
res = requests.get("https://www150.statcan.gc.ca/n1/pub/75-006-x/2019001/article/00006-eng.htm")
res.raise_for_status()
soup=bs4.BeautifulSoup(res.text,'html.parser')
data=soup.select("body > main > section > div > table")

# Take the first list in data and clean it up into a list
good_list=data[0]
new=good_list.getText().strip().split("\n")
list_of_lists=[]

# Split strings at each sentence and then append into a list of lists.
for strings in new[4:114]:
    each_sentence=strings.split(",") 
    if each_sentence != ['']:
        list_of_lists.append(each_sentence)

# Create grid for the graph, 22 rows and 3 columns
empty_list=[]
list_of_lists.insert(3,empty_list) #Need to insert empty list at index 3 to make it equal size of 22x3 grid

# Store list of lists into a file using pickle
my_file=open("stats.pkl","wb")
pickle.dump(list_of_lists,my_file)
my_file.close()

data=list_of_lists

def distribution_count_for_fields_of_study(data):
# From the list of lists, only take the count for the number of first year students 
    count_of_students=data[7::3]
    num_first_year=[]
    for lists in count_of_students:
# Join the numbers to turn them into integers to use for the graph
        separator=""
        total=separator.join(lists)
        total_students=int(total)
        num_first_year.append(total_students)
# Returns a list of integers
    return num_first_year
    

def fields_of_study(data):
# From the list of lists, only take the names of the field of study 
    fields=data[6::3]
    fields_of_study=[]
    for lists in fields:
# Join the names to create a list of strings with the names of all the fields of study
        separator=""
        majors=separator.join(lists)
        fields_of_study.append(majors)
# List of the fields for stem and non stem (only the sub headers)    
    majors=[]
    for field in fields_of_study:
        if field == fields_of_study[2] or field ==fields_of_study[6] or field== fields_of_study[9] or field ==fields_of_study[12]:
            majors.append(field)
    
    return majors


def pie_chart_of_distribution(data):
# Taking only the subheaders to plot the graph
# List of count for the Stem and non stem majors 
    distribution=distribution_count_for_fields_of_study(data)
    count=[]
    for nums in distribution:
        if nums == distribution[2] or nums == distribution[6] or nums==distribution[9] or nums == distribution[12]:
            count.append(nums)

# List of the fields for stem and non stem
    majors=fields_of_study(data)
# Creating a pie chart and exploding the field with the largest percentage of students
    explode=(0,0,0,0.15)
    plt.pie(count, explode=explode, labels=majors, autopct='%1.1f%%', shadow=True)
    plt.title("Distribution of 1st Year Students in All Fields of Study")
# Saving graph to disk
    plt.show()
    plt.savefig("Distribution_of_students_in_field_of_study.png")
    plt.clf() # clear the current figure
    
def percentage_of_women_in_fields_of_study(data):
# From the list of lists, only take the percentage of the number of women in these fields 
    percentage_of_women=data[8::3]
    num_women=[]
    only_major_fields=[]
    for lists in percentage_of_women:
# Join the percentages as a list of strings and not list of lists
        separator=""
        percentage=separator.join(lists)
        num_women.append(percentage)
    for nums in num_women:
        if nums == num_women[2] or nums== num_women[6] or nums == num_women[9] or nums == num_women[12]:
            only_major_fields.append(nums)
        
# Returns a list of strings of percentages
    return only_major_fields

def graph_of_women_represented_in_field(data):
# Turning the list of strings on percentages to list of floats for the graph   
    majors=fields_of_study(data)
    list_of_strings=percentage_of_women_in_fields_of_study(data)
    percentage_of_women=[]
    for nums in list_of_strings:
        num=float(nums)
        percentage_of_women.append(num)
# Finding the percentage of men in the fields to show the comparaison
    percentage_of_men=[]
    for nums in percentage_of_women:
        men=100-float(nums)
        percentage_of_men.append(men)
    
# PLotting the bar chart with the percentage of women in each field of study at the bottom and percentage of men at the top  
    plt.bar(majors, percentage_of_women, color="deeppink",)
    plt.bar(majors, percentage_of_men, bottom=percentage_of_women, color="lightskyblue")
    plt.title("Percentage of Women Compared to Men in All Fields of Study")
    plt.xlabel("Fields of Study")
    plt.ylabel("Percentage Differences")
# Saving graph to disk
    plt.show()
    plt.savefig("Percentage_of_women_represented_in_field.png")
    
         
pie_chart_of_distribution(data)
graph_of_women_represented_in_field(data)













