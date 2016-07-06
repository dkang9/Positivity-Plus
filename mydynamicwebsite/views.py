from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect

from backend.models import *

commonWords = {"the", "went", "be", "and", "of", "to", "a", "in", "today", 
    "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", 
    "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", 
    "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", 
    "what", "so", "if", "go", "make", "can", "like", "has", "had", "got", 
    "happy", "is", "me", "made", "ate", "because", "things","did", "after","finally"}

class HomePage(View):
    def get(self, request):
        context = {}
        context["posts"] = Post.objects.all()[::-1]
        print(context)
        return render(request, 'home.html', context)
        
class MakePost(View):
    def post(self, request):
        text = request.POST.get("post")
        new_post = Post(text=text)
        new_post.save()
        newDict = []
        newDict.append(new_post)
        return HttpResponseRedirect("/bubbles")
        #return render(request, 'bubbles.html',newDict)
        #return HttpResponseRedirect("bubbles.html")

def stripOfPunctuation(string):
    punctuation = "!,.:;{}"
    newString = []
    for letter in string:
        if letter not in punctuation:
            newString.append(letter)
    return "".join(newString)

def topFivePosts(p):
    context = {}
    for sentence in p:
        for word in sentence.split():
            word = word.lower()
            word = stripOfPunctuation(word)
            if word not in commonWords:
                #if "ing" in word:
                #    word = word[:len(word) - 4]
                if context.get(word) == None:
                    context[word] = 45
                else:
                    context[word] += 45
    newList = generateTopFive(context)
    newDict = {}
    for word in newList:
        newDict[word] = context[word]
    return newDict

def generateTopFive(context):
    L = []
    for word in context:
        if len(L) != 5: L.append(word)
        else:
            (result, value) = minValue(L, context)
            if context[word] > value:
                L.remove(result)
                L.append(word)
    return L

def minValue(L, d):
    (result, value) = (L[0], d[L[0]])
    for word in L[1:]:
        if d[word] < value: (result, value) = (word, d[word])
    return (result, value)

def findContainingWord(listOfPosts, dictOfWords):
    dictWithSentences = {}
    for sentence in listOfPosts:
        for word in dictOfWords:
            if word in sentence.lower():
                if dictWithSentences.get(word) == None:
                    dictWithSentences[word] = [sentence]
                else:
                    dictWithSentences[word] += [sentence]
    return dictWithSentences

def putInContext(dict, sentences):
    newDict = {}
    newDict["posts_top"] = []
    id = 0
    for word in dict:
        id += 1
        tempDict = {}
        tempDict["key"] = word
        tempDict["count"] = dict[word]
        tempDict["text"] = sentences[word]
        tempDict["id"] = id
        newDict["posts_top"].append(tempDict)
    return newDict

class Bubbles(View):
    def get(self, request):
        posts = Post.objects.all()
        newList = []
        for post in posts:
            newList.append(post.text)
            print(type(post.text))
        dictTopFivePosts = topFivePosts(newList)
        sentences = findContainingWord(newList, dictTopFivePosts)
        context = putInContext(dictTopFivePosts, sentences)
        return render(request, 'bubbles.html', context)
        
class LookPost(View):
    def get(self, request,variable):
        variable = variable
        posts = Post.objects.all()
        newList = []
        for post in posts:
            newList.append(post.text)
        sentences = findContainingWord(newList, {variable: 0})
        context = {"posts_top": [{"key": variable}, {"text": sentences[variable]}]}
        return render(request, 'posts.html', context)
        
class Sad(View):
    def get(self, request):
        return render(request,'sad.html')