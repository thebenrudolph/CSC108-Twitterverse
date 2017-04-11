import unittest
import twitterverse_functions as tf


class TestGetFilterResults(unittest.TestCase):
    
    def test_get_filter_results_mutation(self):
        """ Confirm get_filter_results does not mutate the parameters it is
        given."""
        
        twitterverse = {'tomCruise': {'following': ['katieH'],\
                                      'web': 'http://www.tomcruise.com', \
                                      'location': 'Los Angeles, CA', \
                                      'bio': 'Official TomCruise.com', \
                                      'name': 'Tom Cruise'}, \
                        'katieH': {'following': ['tomCruise'],\
                                   'web': 'www.tomkat.com', 'location': '',\
                                   'bio': '', 'name': 'Katie Holmes'}, \
                        'benR': {'following': ['katieH', 'tomCruise'], \
                                 'web': 'www.benr.com', 'location': '',\
                                 'bio': '', 'name': 'Ben Rudolph'}}
        usernames = ['benR', 'tomCruise']
        filter_dict = {'following': 'katieH'}
        
        expected = (id(twitterverse), id(usernames), id(filter_dict))
        
        tf.get_filter_results(twitterverse, usernames, filter_dict)
        
        actual = (id(twitterverse), id(usernames), id(filter_dict))
        
        self.assertEqual(actual, expected)
        
    def test_get_filter_results_empty_filter(self):
        """ Test get_filter_results when the filter dictionary is empty. I.e.,
        there are no filters."""
        
        twitterverse = {'tomCruise': {'following': ['katieH'],\
                                        'web': 'http://www.tomcruise.com', \
                                            'location': 'Los Angeles, CA', \
                                            'bio': 'Official TomCruise.com', \
                                              'name': 'Tom Cruise'}, \
                                'katieH': {'following': ['tomCruise'],\
                                    'web': 'www.tomkat.com', 'location': '',\
                                        'bio': '', 'name': 'Katie Holmes'}, \
                                'benR': {'following': ['katieH', 'tomCruise'], \
                                         'web': 'www.benr.com', 'location': '',\
                                         'bio': '', 'name': 'Ben Rudolph'}}
        usernames = ['tomCruise']
        filter_dict = {}
        
        expected = ['tomCruise']
        actual = tf.get_filter_results(twitterverse, usernames, filter_dict)
        
        self.assertEqual(actual, expected)
        
    def test_get_filter_results_one_filter(self):
            """ Test get_filter_results when there is one filter specification,
            that results in at least one username being returned."""
            
            twitterverse = {'tomCruise': {'following': ['katieH'],\
                                        'web': 'http://www.tomcruise.com', \
                                            'location': 'Los Angeles, CA', \
                                            'bio': 'Official TomCruise.com', \
                                                  'name': 'Tom Cruise'}, \
                                    'katieH': {'following': ['tomCruise'],\
                                    'web': 'www.tomkat.com', 'location': '',\
                                        'bio': '', 'name': 'Katie Holmes'}, \
                                'benR': {'following': ['katieH', 'tomCruise'], \
                                        'web': 'www.benr.com', 'location': '',\
                                             'bio': '', 'name': 'Ben Rudolph'}}
            usernames = ['tomCruise', 'benR']
            filter_dict = {'following':'tomCruise'}
            
            expected = ['benR']
            actual = tf.get_filter_results(twitterverse, usernames, filter_dict)
            
            self.assertEqual(actual, expected)        
        
    def test_get_filter_results_multiple_filters(self):
        """ Test get_filter_results when there are multiple filter
        specifications."""
        
        twitterverse = {'tomCruise': {'following': ['katieH'],\
                                            'web': 'http://www.tomcruise.com', \
                                                'location': 'Los Angeles, CA', \
                                            'bio': 'Official TomCruise.com', \
                                                        'name': 'Tom Cruise'}, \
                                        'katieH': {'following': ['tomCruise'],\
                                    'web': 'www.tomkat.com', 'location': '',\
                                        'bio': '', 'name': 'Katie Holmes'}, \
                                'benR': {'following': ['katieH', 'tomCruise'], \
                                        'web': 'www.benr.com', 'location': '',\
                                            'bio': '', 'name': 'Ben Rudolph'}}
        usernames = ['tomCruise', 'benR']
        filter_dict = {'following':'katieH', 'location-includes': 'CA'}
                    
        expected = ['tomCruise']
        actual = tf.get_filter_results(twitterverse, usernames, filter_dict)
                    
        self.assertEqual(actual, expected)
        
        
    def test_get_filter_results_multiple_filters(self):
        """ Test get_filter_results when there are multiple filter
        specifications and multiple usernames."""
        
        twitterverse = {'tomCruise': {'following': ['katieH'],\
                                            'web': 'http://www.tomcruise.com', \
                                                'location': 'Los Angeles, CA', \
                                            'bio': 'Official TomCruise.com', \
                                                        'name': 'Tom Cruise'}, \
                                        'katieH': {'following': ['tomCruise'],\
                                    'web': 'www.tomkat.com', 'location': '',\
                                        'bio': '', 'name': 'Katie Holmes'}, \
                                'benR': {'following': ['katieH', 'tomCruise'], \
                                        'web': 'www.benr.com', 'location': '',\
                                            'bio': '', 'name': 'Ben Rudolph'}}
        usernames = ['tomCruise', 'benR']
        filter_dict = {'following':'katieH', 'location-includes': 'CA'}
                    
        expected = ['tomCruise']
        actual = tf.get_filter_results(twitterverse, usernames, filter_dict)
                    
        self.assertEqual(actual, expected)
        
    def test_get_filter_results_empty_usernames(self):
        """ Test get_filter_results when the usernames list being passed to the
        function is empty."""
        
        twitterverse = {'tomCruise': {'following': ['katieH'],\
                                            'web': 'http://www.tomcruise.com', \
                                                'location': 'Los Angeles, CA', \
                                            'bio': 'Official TomCruise.com', \
                                                        'name': 'Tom Cruise'}, \
                                        'katieH': {'following': ['tomCruise'],\
                                    'web': 'www.tomkat.com', 'location': '',\
                                        'bio': '', 'name': 'Katie Holmes'}, \
                                'benR': {'following': ['katieH', 'tomCruise'], \
                                        'web': 'www.benr.com', 'location': '',\
                                            'bio': '', 'name': 'Ben Rudolph'}}
        usernames = []
        filter_dict = {'following':'katieH', 'location-includes': 'CA'}
                            
        expected = []
        actual = tf.get_filter_results(twitterverse, usernames, filter_dict)
                            
        self.assertEqual(actual, expected)
        
    def test_get_filter_results_filter_returns_no_usernames(self):
        """ Test get_filter_results when the filter dictionary filters out
        all of the usernames in the list."""
        
        twitterverse = {'tomCruise': {'following': ['katieH'],\
                                            'web': 'http://www.tomcruise.com', \
                                                'location': 'Los Angeles, CA', \
                                            'bio': 'Official TomCruise.com', \
                                                        'name': 'Tom Cruise'}, \
                                        'katieH': {'following': ['tomCruise'],\
                                    'web': 'www.tomkat.com', 'location': '',\
                                        'bio': '', 'name': 'Katie Holmes'}, \
                                'benR': {'following': ['katieH', 'tomCruise'], \
                                        'web': 'www.benr.com', 'location': '',\
                                            'bio': '', 'name': 'Ben Rudolph'}}        
        
        usernames = ['tomCruise', 'benR']
        filter_dict = {'following':'katieH', 'location-includes': 'Peru'}
                            
        expected = []
        actual = tf.get_filter_results(twitterverse, usernames, filter_dict)
                            
        self.assertEqual(actual, expected)        
    
if __name__ == '__main__':
    unittest.main(exit=False)
