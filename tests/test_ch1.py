#  Write a function that takes a string argument
#  and returns the number of vowels in it

from selenium import webdriver

# Optional argument, if not specified will search path
driver = webdriver.Chrome('D:\Google Drive\Continuous Education\Python\Tutorials\selenium_drivers')

def vowel_count(string):
    vowels = ["a", "e", "i", "o", "u"]
    count = 0
    for ch in string.lower():
        if ch in vowels:
            count += 1
    return count


def test_first_name():
    assert vowel_count('vadim') == 2


def test_last_name():
    assert vowel_count('blaker') == 2


def test_upper_case():
    assert vowel_count("VADIM BLAKER") == 4
