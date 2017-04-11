
# Write your Twitterverse functions here
def process_data(file):
    """(file open for reading) -> dict of {str: dict of {str: object}}
    
    Read the file open for reading and return the data in the Twitterverse,
    dictionary format. 
    """
    # Initalize twitterverse dictionary
    twitterverse = {}
    
    # Read file into a list
    list_of_lines = file_to_list(file)
    
    start = 0
    end = 0
    for i in range(len(list_of_lines)):
        #if the line is "END" signifies end of user info, send info to be
        #processed, and then add indivudal userinfo to twitterverse
        if list_of_lines[i] == "END": 
            end = i
            user_info = list_of_lines[start + 1 : end]
            twitterverse[list_of_lines[start]
                         ] = create_username_dictionary(user_info)
            start = i + 1
    return twitterverse        
            

def create_username_dictionary(user_info):
    """ (list of str) -> dict of {str: object}}
    
    Return an individual user dictionary to be entered to the twitterverse,
    dictionary based off the data from user_info.
    
    >>> user_info = ['Tom Cruise', 'Los Angeles, CA', \
    'http://www.tomcruise.com', 'Official TomCruise.com crew tweets.',\
    'Visit us at Facebook!', 'ENDBIO', 'katieH']
    >>> create_username_dictionary(user_info) == {'name': 'Tom Cruise',\
    'bio': 'Official TomCruise.com crew tweets.\\nVisit us at Facebook!',\
    'location': 'Los Angeles, CA', 'web': 'http://www.tomcruise.com',\
    'following': ['katieH']}
    True
    >>> user_info = ['Katie Holmes','', 'www.tomkat.com', '', 'ENDBIO',\
    'tomCruise']
    >>> expected = {'name': 'Katie Holmes', 'bio': '', 'location': '',\
    'web': 'www.tomkat.com', 'following': ['tomCruise']}
    >>> create_username_dictionary(user_info) == expected
    True
    """
    user = {}
    user['bio'] = ""
    i = 0
    
    while user_info[i] != "ENDBIO": #stop loop when 'ENDBIO' is the line
        if i == 0:
            user['name'] = user_info[i]
        elif i == 1:
            user['location'] = user_info[i]
        elif i == 2:
            user['web'] = user_info[i]
        else:
            user['bio'] += user_info[i]+"\n"
        i += 1
    user['bio'] = user['bio'][:-1]
    user = add_following_to_dict(user, user_info, i)        

    return user

def add_following_to_dict(user, user_info, i):
    """ (dict of {str: object}}, list of str, int) -> dict of {str: object}}
    
    Add the 'following' key into the user dictionary by reading the information 
    in, user_info starting at the index where the previous function left of, 
    at i.
    
    >>> user = {'web': '', 'location': '', \
    'name': 'Katie Holmes', 'bio': ''}
    >>> user_info = ['Katie Holmes','', '', '', 'ENDBIO', 'tomCruise']
    >>> i = 4
    >>> add_following_to_dict(user, user_info, i) == {'name': 'Katie Holmes',\
    'bio': '', 'location': '', 'web': '', 'following': ['tomCruise']}
    True
    >>> user = {'location': 'Los Angeles, CA', 'name': 'Tom Cruise',\
    'web': '', 'bio': ''}
    >>> user_info = ['Tom Cruise', 'Los Angeles, CA', '', '', '',\
    'ENDBIO', 'katieH']
    >>> i = 5
    >>> add_following_to_dict(user, user_info, i) == {'location':\
    'Los Angeles, CA', 'name': 'Tom Cruise', 'following': ['katieH'], \
    'web': '', 'bio': ''}
    True
    """
    
    user['following'] = []
    
    for i in range(i + 1, len(user_info)):
            if user_info[i] != 'ENDBIO':
                user['following'].append(user_info[i])
    return user            

def file_to_list(file):
    """ (file open for reading) -> list of str
    
    Read the file open for reading and return each line as a new str item in a,
    list.
    """
    
    list_of_lines = []
    
    for line in file:
        list_of_lines.append(line.strip())# strip line of any spaces or \n
    
    return list_of_lines

def process_query(file):
    """ (file open for reading) -> dict of {str: dict of {str: object}}
    
    Read the file open for reading and create the querydictionary from the data.
    """
    query_dictionary = {}
    
    #read in data and sort by search, filter, and present keys
    data = file_to_list(file)
    search_list = data[1:data.index("FILTER")]
    filter_list = data[data.index("FILTER")+1:data.index("PRESENT")]
    present_list = data[data.index("PRESENT")+1:]
    
    #add to query_dictionary
    query_dictionary['search'] = add_search_key(search_list)
    query_dictionary['filter'] = add_filter_present_key(filter_list)
    query_dictionary['present'] = add_filter_present_key(present_list)
    
    return query_dictionary

def add_search_key(data):
    """(list of str) -> search specification dictionary
    
    Return the search key for the query dictionary by creating the search,
    specification dictionary.
    
    >>> data =['tomCruise', 'following']
    >>> add_search_key(data) == {'username': 'tomCruise',\
    'operations': ['following']}
    True
    >>> data =['tomCruise', 'followers', 'followers']
    >>> add_search_key(data) == {'username': 'tomCruise',\
    'operations': ['followers', 'followers']}
    True
    """
    search = {}
    search['username'], search['operations'] = data[0], []
    
    for i in range(1,len(data)):
        search['operations'].append(data[i])
    
    return search

def add_filter_present_key(data):
    """(list of str) -> dict of {str: str}
    
    Return the filter key for the querydictionary by creating the filter or
    present dictionary.
    
    >>> data = ['sort-by popularity', 'format short']
    >>> add_filter_present_key(data) == {'sort-by': 'popularity',\
    'format': 'short'}
    True
    >>> data = ['following KatieH', 'location-includes USA']
    >>> add_filter_present_key(data) == {'following': 'KatieH',\
    'location-includes': 'USA'}
    True
    """
    key = {}
    
    for i in range(len(data)):
        current = data[i].split()
        key[current[0]] = current[1]
    
    return key

def all_followers(twitterverse, username):
    """ (Twitterverse dictionary, str) -> list of str
    
    Return a list of usernames that are following the username,
    by seraching through the twitterverse dictionary.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes',\
    'following': ['tomCruise'], 'web': 'www.tomkat.com', 'bio': ''},\
    'tomCruise': {'location': 'Los Angeles, CA', 'name': 'Tom Cruise',\
    'following': ['katieH'], 'web': 'http://www.tomcruise.com',\
    'bio': 'Official TomCruise.com crew tweets.\\nVisit us at Facebook!'},\
    'benR': {'location': '', 'name': 'Ben Rudolph', 'following':\
    ['katieH', 'tomCruise'], 'web': 'www.benr.com', 'bio': ''}}
    >>> all_followers(twitterverse, 'tomCruise')
    ['benR', 'katieH']
    >>> all_followers(twitterverse, 'benR')
    []
    """
    
    result = []
    # find people who are following the specific username
    for item in twitterverse:
        
        if username in twitterverse[item]['following']:
            result.append(item)
    
    result.sort()        
    return result

def all_following(twitterverse, username):
    """ (Twitterverse dictionary, str) -> list of str
    
    Return a list of usernames that the username is following,
    searching through the twitterverse dictionary.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes',\
    'following': ['tomCruise'], 'web': 'www.tomkat.com', 'bio': ''},\
    'tomCruise': {'location': 'Los Angeles, CA', 'name': 'Tom Cruise',\
    'following': ['katieH'], 'web': 'http://www.tomcruise.com',\
    'bio': 'Official TomCruise.com crew tweets. We love you guys!'},\
    'benR': {'location': '', 'name': 'Ben Rudolph', 'following':\
    [], 'web': 'www.benr.com', 'bio': ''}}
    >>> all_following(twitterverse, 'tomCruise')
    ['katieH']
    >>> all_following(twitterverse, 'benR')
    []
    """
    # return list of people who username is following
    result = twitterverse[username]['following']
    result.sort()
    return result

def get_search_results(twitterverse, search_dictionary):
    """ (Twitterverse dictionary, search specification dictionary) -> 
    list of str
    
    Return a list of usernames that result from the search_dictionary being 
    applied to the data in twitterverse.
    
    >>> twitterverse = {'c': {'location': 'Kansas', 'bio': '', 'following':\
    ['f'], 'name': 'The Captain', 'web': 'kellogs.com'}, 'h': {'location': '',\
    'bio': '', 'following': ['k'], 'name': '', 'web': ''}, 'b': {'location':\
    'New York', 'bio': 'Running in Central Park. Reading in Bryant Park.', \
    'following': ['tomCruise'], 'name': 'Brian K.', 'web': ''}, 'k': \
    {'location': '', 'bio': '', 'following': [], 'name': '', 'web': ''}, \
    'd': {'location': 'London, UK', 'bio': '', 'following': ['f', 'g', 'h'],\
    'name': 'Daniel A.', 'web': ''}, 'j': {'location': 'Ottawa', 'bio': '',\
    'following': [], 'name': '', 'web': ''}, 'e': {'location': 'New Brunswick',\
    'bio': 'Movies! Popcorn!', 'following': ['b'], 'name': 'Eleanor', 'web':\
    ''}, 'f': {'location': '', 'bio': '', 'following': [], 'name': '', 'web':\
    ''}, 'g': {'location': 'Barcelona', 'bio': 'Loves Coding + Surfing!',\
    'following': ['i', 'j', 'h'], 'name': 'Gabriella H.', 'web': ''}, \
    'tomCruise': {'location': 'Los Angeles, CA', 'bio': \
    'Official TomCruise.com crew tweets.\\nVisit us at Facebook!', 'following':\
    ['c', 'd', 'e'], 'name': 'Tom Cruise', 'web': 'http://www.tomcruise.com'},\
    'i': {'location': 'Toronto', 'bio': '', 'following': [], 'name': '', 'web':\
    ''}, 'a': {'location': 'Seattle, WA', 'bio': 'Love hiking!', 'following':\
    ['tomCruise', 'c'], 'name': 'Andrew', 'web': ''}}
    >>> search_dictionary = {'username': 'tomCruise', 'operations':\
    ['following', 'following', 'following']}
    >>> get_search_results(twitterverse, search_dictionary)
    ['h', 'i', 'j', 'k', 'tomCruise']
    >>> search_dictionary = {'username': 'tomCruise', 'operations':\
    ['followers']}
    >>> get_search_results(twitterverse, search_dictionary)
    ['a', 'b']
    """
    
    result = [search_dictionary['username']]    
    # complete all operations in the search dictionary
    for item in search_dictionary['operations']:
        
        operation_result = []
        
        # if operation is 'following'
        if item == 'following':
            for name in result:
                operation_result.extend(all_following(twitterverse, name))

            
        # if operation is 'follower'    
        elif item == 'followers':
            for name in result:
                operation_result.extend(all_followers(twitterverse, name))
                
        # remove duplicates from the list
        result = remove_duplicates(operation_result)
    
    result.sort()    
    return result    

def remove_duplicates(data):
    """ (list of str) -> list of str
    
    Return a new list of data with its duplicate values removed
    
    >>> remove_duplicates(['a', 'b', 'a', 'c'])
    ['a', 'b', 'c']
    >>> remove_duplicates([])
    []
    """
    
    # return a list with duplicate usernames removed
    result = list(set(data))
    result.sort()
    return result

def get_filter_results(twitterverse, usernames, filter_dictionary):
    """ (Twitterverse dictionary, list of str, filter specification dictionary)
    -> list of str
    
    Apply the specified filters from filter_dictionary to the given usernames to 
    determine which usernames to meet specifed requirements, and return the 
    resulting list of usernames by checking with data in twitterverse.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes',\
    'following': ['tomCruise'], 'web': 'www.tomkat.com', 'bio': ''}, \
    'tomCruise': {'location': 'Los Angeles, CA', 'name': 'Tom Cruise', \
    'following': ['katieH'], 'web': 'http://www.tomcruise.com', 'bio': \
    'Official TomCruise.com crew tweets.\\nVisit us at Facebook!'}, \
    'benR': {'location': 'Toronto', 'name': 'Ben Rudolph', 'following': \
    ['katieH', 'tomCruise'], 'web': 'www.benr.com', 'bio': ''}}
    >>> usernames = ['tomCruise', 'katieH']
    >>> filter_dictionary = {'location-includes': 'CA'}
    >>> get_filter_results(twitterverse, usernames, filter_dictionary)
    ['tomCruise']
    >>> usernames = ['benR', 'katieH']
    >>> filter_dictionary = {'location-includes': 'Canada', 'following':\
    'tomCruise'}
    >>> get_filter_results(twitterverse, usernames, filter_dictionary)
    []
    """
    
    results = usernames[:]
    
    for key in filter_dictionary:
        filter_result = []
        if key == 'name-includes':# send to name_filter function
            filter_result.extend(name_filter(twitterverse, results, 
                                                      filter_dictionary[key]))
        elif key == 'location-includes':# send to location_filter function
            filter_result.extend(location_filter(twitterverse, results, 
                                                 filter_dictionary[key]))
        elif key == 'following':# send to following_filter function
            filter_result.extend(following_filter(twitterverse, results, 
                                                 filter_dictionary[key]))
        elif key == 'follower':# send to follower_filter function
            filter_result.extend(follower_filter(twitterverse, results, 
                                                 filter_dictionary[key]))           
        results = filter_result
       
    return results

def name_filter(twitterverse, usernames, filter_name):
    """(Twitterverse dictionary, list of str, str) -> list of str
    
    Apply the specified filter_name to the given usernames to determine which 
    usernames to meet specifed requirements, and return the resulting list of 
    usernames by checking with data in twitterverse.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes', \
    'following': ['tomCruise', 'benR'], 'web': 'www.tomkat.com', 'bio': ''}, \
    'tomCruise': {'location': 'Los Angeles, CA', 'name': 'Tom Cruise', \
    'following': ['katieH'], 'web': 'http://www.tomcruise.com', 'bio': \
    'Official TomCruise.com crew tweets.\\nVisit us at Facebook!'},\
    'benR': {'location': 'Toronto', 'name': 'Ben Rudolph', 'following': \
    ['katieH', 'tomCruise'], 'web': 'www.benr.com', 'bio': ''}}
    >>> usernames = ['tomCruise', 'benR']
    >>> filter_name = 'Tom'
    >>> name_filter(twitterverse, usernames, filter_name)
    ['tomCruise']
    >>> filter_name = 'Benjamin'
    >>> name_filter(twitterverse, usernames, filter_name)
    []
    """
       
    result = []
    
    #loop through usernames and append them to results if their name includes
    #specific name in the filter
    for item in usernames:
        
        if filter_name.lower() in twitterverse[item]['name'].lower():
            result.append(item)
    
    return result

def location_filter(twitterverse, usernames, filter_location):
    """(Twitterverse dictionary, list of str, str) -> list of str
    
    Apply the specified filter_location to the given usernames to determine 
    which usernames to meet specifed requirements, and return the resulting 
    list of usernames by checking data in twitterverse.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes',\
    'following': ['tomCruise', 'benR'], 'web': 'www.tomkat.com', 'bio': ''}, \
    'tomCruise': {'location': 'Los Angeles, CA', 'name': 'Tom Cruise', \
    'following': ['katieH'], 'web': 'http://www.tomcruise.com', 'bio': \
    'Official TomCruise.com crew tweets.\\nVisit us at Facebook!'}, \
    'benR': {'location': 'Toronto, Canada', 'name': 'Ben Rudolph', \
    'following': ['katieH', 'tomCruise'], 'web': 'www.benr.com', 'bio': ''}}
    >>> usernames = ['tomCruise', 'benR']
    >>> filter_location = 'Italy'
    >>> location_filter(twitterverse, usernames, filter_location)
    []
    >>> filter_location = 'CA'
    >>> location_filter(twitterverse, usernames, filter_location)
    ['tomCruise', 'benR']
    """
    
    result = []
    
    # loop through usernames, append to result if their location information
    # contains the filter_location
    for item in usernames:
        if filter_location.lower() in twitterverse[item]['location'].lower():
            result.append(item)
    
    return result

def following_filter(twitterverse, usernames, filter_following):
    """(Twitterverse Dictionary, list of str, str) -> list of str
        
    Applies the specified filter_following to the given usernames to determine 
    which usernames to meet specifed requirements, and retursn the resulting 
    list of usernames by checking data in twitterverse.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes',\
    'following': ['tomCruise', 'benR'], 'web': 'www.tomkat.com', 'bio': ''},\
    'tomCruise': {'location': 'Los Angeles, CA', 'name': 'Tom Cruise', \
    'following': ['katieH'], 'web': 'http://www.tomcruise.com', \
    'bio': 'Official TomCruise.com crew tweets.\\nVisit us at Facebook!'}, \
    'benR': {'location': 'Toronto', 'name': 'Ben Rudolph',\
    'following': ['katieH', 'tomCruise'], 'web': 'www.benr.com', 'bio': ''}}
    >>> usernames = ['benR', 'katieH']
    >>> filter_following = 'tomCruise'
    >>> following_filter(twitterverse, usernames, filter_following)
    ['benR', 'katieH']
    >>> usernames = ['tomCruise', 'katieH']
    >>> filter_following = 'BenR'
    >>> following_filter(twitterverse, usernames, filter_following)
    []
    """
    
    result = []
    
    # loop through usernames list and append username to result if they are
    # following the specific user name in the filter
    for item in usernames:
        if filter_following in twitterverse[item]['following']:
            result.append(item)
                
    return result

def follower_filter(twitterverse, usernames, filter_follower):
    """(Twitterverse dictionary, list of str, str) -> list of str
        
    Apply the specified filter_follower to the given usernames to determine 
    which usernames  meet specifed requirements, and return the resulting 
    list of usernames by checking data in twitterverse.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes',\
    'following': ['tomCruise', 'benR'], 'web': 'www.tomkat.com', 'bio': ''},\
    'tomCruise': {'location': 'Los Angeles, CA', 'name': 'Tom Cruise', \
    'following': ['katieH'], 'web': 'http://www.tomcruise.com', 'bio': \
    'Official TomCruise.com crew tweets.\\nVisit us at Facebook!'}, \
    'benR': {'location': 'Toronto', 'name': 'Ben Rudolph', \
    'following': ['katieH', 'tomCruise'], 'web': 'www.benr.com', 'bio': ''}}
    >>> usernames = ['benR', 'katieH']
    >>> filter_follower = 'tomCruise'
    >>> follower_filter(twitterverse, usernames, filter_follower)
    ['katieH']
    >>> usernames = ['benR']
    >>> follower_filter(twitterverse, usernames, filter_follower)
    []
    """ 
    
    result = []
    
    # loop through usernames, append to result if the follower_filter is
    # following the current username
    
    if filter_follower in twitterverse:
        
        for item in usernames:
            if item in twitterverse[filter_follower]['following']:
                result.append(item)
        return result        
                
    else: # if username is not in twitterverse return empty list
        return result

def get_present_string(twitterverse, usernames, present_dict):
    """(Twitterverse dictionary, list of str, presentation specification
    dictionary) -> str
    
    Format the results for presentation based on the given presentation 
    specification in present_dict and return the formatted usernames with
    appropriate information and data from twitterverse.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes',\
    'following': ['tomCruise'], 'web': '', 'bio': ''},\
    'benR': {'location': '', 'name': 'Ben Rudolph',\
    'following': ['katieH'], 'web': '', 'bio': ''}}
    >>> usernames = ['benR', 'katieH']
    >>> present_dict = {'sort-by':'popularity', 'format': 'short'}
    >>> get_present_string(twitterverse, usernames, present_dict)
    "['katieH', 'benR']"
    >>> usernames = []
    >>> present_dict = {'sort-by':'popularity', 'format': 'long'}
    >>> get_present_string(twitterverse, usernames, present_dict)
    '----------\\n----------\\n'
    """
    
    results = usernames[:]
    # sort the usernames by specification
    sort_usernames(twitterverse, results, present_dict['sort-by'])
    
    # create string representation of data
    presentation = represent_data(twitterverse, results, present_dict['format'])
    
    return presentation

def sort_usernames(twitterverse, usernames, sort):
    """(Twitterverse dictionary, list of str, str) -> NoneType
    
    Return a sorted list of the usernames, based on the specific sort 
    parameter by analyzing data from twitterverse.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes',\
    'following': ['tomCruise', 'benR'], 'web': 'www.tomkat.com', 'bio': ''},\
    'tomCruise': {'location': 'Los Angeles, CA', 'name': 'Tom Cruise', \
    'following': ['katieH'], 'web': 'http://www.tomcruise.com', 'bio': \
    'Official TomCruise.com crew tweets.\\nVisit us at Facebook!'}, \
    'benR': {'location': 'Toronto', 'name': 'Ben Rudolph', \
    'following': ['katieH', 'tomCruise'], 'web': 'www.benr.com', 'bio': ''}}
    >>> usernames = ['benR', 'katieH']
    >>> sort = 'popularity'
    >>> sort_usernames(twitterverse, usernames, sort)
    >>> usernames
    ['katieH', 'benR']
    >>> usernames = ['tomCruise', 'katieH']
    >>> sort = 'name'
    >>> sort_usernames(twitterverse, usernames, sort)
    >>> usernames
    ['katieH', 'tomCruise']
    """
       
    if sort == 'username':
        tweet_sort(twitterverse, usernames, username_first)
    elif sort == 'name':
        tweet_sort(twitterverse, usernames, name_first)
    else:    
        tweet_sort(twitterverse, usernames, more_popular)

def represent_data(twitterverse, results, present_format):
    """(Twitterverse dictionary, list of str, str) -> str
    
    Return a string representation of the usernames in results in the format,
    specified by the present_format (long or short) with information from
    twitterverse.
    
    >>> twitterverse = {'katieH': {'location': '', 'name': 'Katie Holmes',\
    'following': ['tomCruise', 'benR'], 'web': 'www.tomkat.com', 'bio': ''},\
    'tomCruise': {'location': 'Los Angeles, CA', 'name': 'Tom Cruise', \
    'following': ['katieH'], 'web': 'http://www.tomcruise.com', 'bio': \
    'Official TomCruise.com crew tweets.\\nVisit us at Facebook!'}, \
    'benR': {'location': 'Toronto', 'name': 'Ben Rudolph', \
    'following': ['katieH', 'tomCruise'], 'web': 'www.benr.com', 'bio': ''}}
    >>> results = ['katieH']
    >>> present_format = 'long'
    >>> represent_data(twitterverse, results, present_format)
    "----------\\nkatieH\\nname: Katie Holmes\\nlocation: \\nwebsite: www.tomkat.com\\nbio:\\n\\nfollowing: ['tomCruise', 'benR']\\n----------\\n"
    >>> present_format = 'short'
    >>> represent_data(twitterverse, results, present_format)
    "['katieH']"
    
    """
    #short form presentation
    if present_format == 'short':
        result = list_to_string(results)
    #long form presentation
    else:
        result = long_format(twitterverse, results)
    
    return result

def long_format(twitterverse, data):
    """(Twitterverse dictionary, list of str) -> str
    
    Return a string representation of the usernames from data, and their
    information from the twitterverse dictionary.
    
    >>> twitterverse = {'a':{'name': 'a', 'location':'', 'web':'', 'bio': '',\
    'following':[]}}
    >>> data = ['a']
    >>> long_format(twitterverse, data)
    '----------\\na\\nname: a\\nlocation: \\nwebsite: \\nbio:\\n\\nfollowing: []\\n----------\\n'
    >>> twitterverse = {'a':{'name': 'CS', 'location':'T', 'web':'', 'bio': '',\
    'following':[]}}
    >>> data = []
    >>> long_format(twitterverse, data)
    '----------\\n----------\\n'
    """
    
    end = '----------\n'
    present = end
    
    if data == []:
        present += end
        
    else:    
        for username in data:
            present += \
                username + '\n' + 'name: ' + twitterverse[username]['name']\
            + '\n' + 'location: ' + twitterverse[username]['location'] + '\n'\
            + 'website: ' + twitterverse[username]['web'] + '\n' + 'bio:\n'\
            + twitterverse[username]['bio'] + '\n' + 'following: ' +\
            list_to_string(twitterverse[username]['following']) + '\n' + end
        
    return present    
    
def list_to_string(data):
    """(list of str) -> str
    
    Return a string representation of data.
    
    >>> list_to_string(['a', 'b', 'c'])
    "['a', 'b', 'c']"
    >>> list_to_string([])
    '[]'
    """
    
    result = '['
    
    for item in data:
        result += "'" + item + "', "
    if len(result) > 1:
        result = result[:-2]
    result += ']'
    
    return result

# --- Sorting Helper Functions ---
def tweet_sort(twitter_data, results, cmp):
    """ (Twitterverse dictionary, list of str, function) -> NoneType
    
    Sort the results list using the comparison function cmp and the data in 
    twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> result_list = ['c', 'a', 'b']
    >>> tweet_sort(twitter_data, result_list, username_first)
    >>> result_list
    ['a', 'b', 'c']
    >>> tweet_sort(twitter_data, result_list, name_first)
    >>> result_list
    ['b', 'a', 'c']
    """
    
    # Insertion sort
    for i in range(1, len(results)):
        current = results[i]
        position = i
        while position > 0 and cmp(twitter_data, results[position - 1], current) > 0:
            results[position] = results[position - 1]
            position = position - 1 
        results[position] = current  
            
def more_popular(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return -1 if user a has more followers than user b, 1 if fewer followers, 
    and the result of sorting by username if they have the same, based on the 
    data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> more_popular(twitter_data, 'a', 'b')
    1
    >>> more_popular(twitter_data, 'a', 'c')
    -1
    """
    
    a_popularity = len(all_followers(twitter_data, a)) 
    b_popularity = len(all_followers(twitter_data, b))
    if a_popularity > b_popularity:
        return -1
    if a_popularity < b_popularity:
        return 1
    return username_first(twitter_data, a, b)
    
def username_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return 1 if user a has a username that comes after user b's username 
    alphabetically, -1 if user a's username comes before user b's username, 
    and 0 if a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> username_first(twitter_data, 'c', 'b')
    1
    >>> username_first(twitter_data, 'a', 'b')
    -1
    """
    
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def name_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
        
    Return 1 if user a's name comes after user b's name alphabetically, 
    -1 if user a's name comes before user b's name, and the ordering of their
    usernames if there is a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> name_first(twitter_data, 'c', 'b')
    1
    >>> name_first(twitter_data, 'b', 'a')
    -1
    """
    
    a_name = twitter_data[a]["name"]
    b_name = twitter_data[b]["name"]
    if a_name < b_name:
        return -1
    if a_name > b_name:
        return 1
    return username_first(twitter_data, a, b)       


if __name__ == '__main__':
    import doctest
    doctest.testmod()
