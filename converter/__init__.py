import json
import sys
from operator import attrgetter, itemgetter
import datetime
import email.utils
import time

def get_time_from_email(my_time):
    a = email.utils.parsedate_tz(my_time)
    crapp = datetime.datetime(*a[:6]) - datetime.timedelta(seconds= a[-1]);
    return time.mktime(crapp.timetuple())

def remove_bad(line):
    returner = line.replace("Re: ", "", 1)
    returner = returner.replace("RE: ", "", 1)
    returner = returner.replace("FWD: ", "", 1)
    returner = returner.replace("Fwd: ", "", 1)
    returner = returner.replace("[CORRECTION] Re: ", "", 1) 
    returner = returner.replace("FW: ", "", 1) 
    returner = returner.replace("Fw: ", "", 1) 
    return returner

def my_getter(my_i):
    return get_time_from_email(my_i['Date'])

def main(argv):

    unique_subjects = []
    json_data = json.load(open("json_data.txt",'r'))
    json_data = sorted(json_data, key=my_getter)
    for row in json_data:
        subject_full = row['Subject']
        subject_good = remove_bad(subject_full)
        
        if (subject_good not in unique_subjects):
            unique_subjects.append(subject_good)
    #print unique_subjects
    width = len(unique_subjects)
    #print width
    
    subject_dict = dict.fromkeys(unique_subjects, 0)
    for row in json_data:
        subject_full = row['Subject']
        subject_good = remove_bad(subject_full)
        subject_dict[subject_good] = subject_dict[subject_good] + 1
    #0, name, tag, subgroup, group
    height = max(subject_dict.values())
    #print height
    final_data = []
    i = 0
    while i < height:
        final_data.append([])
        j = 0
        while j < width:
            final_data[i].append([0])
            j = j + 1
        i = i + 1
        

    #for rowish in final_data:
    #    print rowish
    p = 0
    for curr_subject in unique_subjects:
        curr_end = height - 1
        for row in json_data:
            subject_full = row['Subject']
            subject_good = remove_bad(subject_full)
            if(subject_good == curr_subject):
                subgroup = ''
                try:
                    subgroup = row['Subgroup']
                except KeyError:
                    subgroup = row['Group']
                name_alone = row['From'].partition("<")[0];
                if(name_alone.find(',')):
                    sections = name_alone.partition(',')
                    name_alone = sections[2] + " " + sections[0]
                final_data[curr_end][p] = [1, name_alone, row['Tag'], subgroup, row['Group'], remove_bad(row['Subject']), get_time_from_email(row['Date'])]
                curr_end = curr_end - 1
        p = p + 1

    
    # get unique groups
    unique_groups = []
    for row in json_data:
        group = row['Group']
        
        if (group not in unique_groups):
            unique_groups.append(group)
            
    # get unique subgroups
    unique_subgroups = []
    for row in json_data:
        subgroup = ''
        try:
            subgroup = row['Subgroup']
        except KeyError:
            subgroup = row['Group']
        
        if (subgroup not in unique_subgroups):
            unique_subgroups.append(subgroup)
    
    # get unique tags
    unique_tags = []
    for row in json_data:
        tag = row['Tag']
        
        if (tag not in unique_tags):
            unique_tags.append(tag)
            
            
            
    true_final_data = []
    i = 0
    while i < height:
        true_final_data.append([])
        j = 0
        while j < width:
            true_final_data[i].append([0])
            j = j + 1
        i = i + 1
    
    m = 0
    for g in unique_groups:
        for s in unique_subgroups:
            for t in unique_tags:
                i = 0
                while i < len(final_data[len(final_data) - 1]):
                    curr = final_data[len(final_data) - 1][i]
                    if(curr[4] == g and curr[3] == s and curr[2] == t):
                        h = 0
                        while (h < len(true_final_data)):
                            true_final_data[h][m] = final_data[h][i]
                            h = h + 1
                        m = m + 1
                        #copy all rows of data
                    i = i + 1
    # sort by groups, subgroups, and tags

    #sort by time


    print '['
    for rowish in true_final_data:
        print rowish , ','
    print ']'

    print ''
    print ''
    print ''
    
    #sort each wedge section by group
    subgroups_order = ['Undergrad','PhD','HCI','SC','LIS','ARM','PI','CI','IPOL','TAL','IAR', 'HI', 'IEM', 'Staff', 'Faculty', 'Alumni', 'Other']
    
    alt_data = []
    i = 0
    while i < height:
        alt_data.append([])
        j = 0
        while j < width:
            alt_data[i].append([0])
            j = j + 1
        i = i + 1
    
       
    i = 0
    while i < len(true_final_data[len(true_final_data) - 1]):
        m = len(true_final_data) - 1
        j = subgroups_order.index(true_final_data[len(true_final_data) - 1][i][3])
        length = len(subgroups_order) + j
        q = j
        while q < length:
            k = len(true_final_data) - 1
            while k > -1:
                if(len(true_final_data[k][i]) > 1):
                    subg = true_final_data[k][i][3]
                    if(subg == subgroups_order[q % len(subgroups_order)]):
                        alt_data[m][i] = true_final_data[k][i]
                        m = m - 1
                k = k - 1
            q = q + 1
        i = i + 1
            
    print '['
    for rowish in alt_data:
        print rowish , ','
    print ']'



if __name__ == '__main__':
    main(sys.argv)