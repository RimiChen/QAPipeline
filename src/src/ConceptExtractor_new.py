'''
This file provides fast, simple extraction of Rensa assertions from natural text, which may help you write simple assertions in natural text instead of JSON.

Advanced users may want to look into more thorough extractors (e.g. Fader et al., 2011: "Identifying relations for open information extraction") or build their own.
'''

import sys
import os
import json
import pprint
import en
#import regular expression
import re
from Entity import *



# Returns a list of story assertions gleaned from the string s.
def test_rensa_functions():
    print("Successfully import rensa functinos")

def extract_story_concepts(s):
    actors, assertions = [], []
    extractActors = extract_actors(assertions, s)
    actors = extractActors[0]
    assertions = extractActors[1]
    sentences = split_sentences(s)
    for sp,e in enumerate(sentences):
        assertions = extract_basic_properties(assertions, e, sp)
        assertions = extract_actor_actions(assertions, actors, e, sp)
        assertions = extract_actor_properties(assertions, actors, e, sp)
    return assertions

####R get entities in the story.
def extract_entities(assertions, s):
    ####print(en.sentence.tag(s))
    items = []
    # Check for general nouns that are known names.
    #matches = en.sentence.find(s, "NN")
    
    ####R name is in NNP
    matches = en.sentence.find(s, "NN")
    ####R
    #print(matches)
    for match in matches:
        name = match[0][0]
        if not baby_names.__contains__(name):
            if name not in items and not name.isdigit():
                items.append(name)
                newAssertions = [
                    {"l":[name], "relation":"instance_of","r":["entity"]}
                ]
                assertions.extend([x for x in newAssertions if x not in assertions])
    return [items, assertions]


# Determine the actors present in the story.
def extract_actors(assertions, s):
    #print(en.sentence.tag(s))
    actors = []
  
    ####R name is in NNP
    matches = en.sentence.find(s, "NNP")

    ####R
    #print(matches)
    for match in matches:
        name = match[0][0]
        if baby_names.__contains__(name):
            if name not in actors:
                actors.append(name)
                gender = guess_gender(name)
                newAssertions = [
                    {"l":[name], "relation":"instance_of","r":["actor"]},
                    {"l":[name], "relation":"has_gender","r":[gender]}
                ]
                assertions.extend([x for x in newAssertions if x not in assertions])
    return [actors, assertions]

####R get entities in the story.
def extract_location(assertions, s):
    #print(en.sentence.tag("from the room, here, there, down"))
    #print(en.sentence.tag(s))
    locations = []
    # Check for general nouns that are known names.
    #matches = en.sentence.find(s, "NN")
    
    ####R name is in NNP
    matches = en.sentence.find(s, "IN (DT) NN")
    matches += en.sentence.find(s, "TO (DT) NN")
    #matches += 
    ####R
    #print(matches)
    for match in matches:
        name = match[2][0]
        relation = match[0][0]
        if not match[0][0] == "up" and not match[0][0] == "down":
            ####R for cases like pick up(IN) the(DT) apple(NN)  
            if name not in locations :
                locations.append(name)
                newAssertions = [
                    {"l":[name], "relation":relation,"r":["location"]}
                ]
                assertions.extend([x for x in newAssertions if x not in assertions])

    matches = en.sentence.find(s, "(DT) NN EX")
    matches += en.sentence.find(s, "(DT) NN EX")
    #matches += 
    ####R
    #print(matches)
    for match in matches:
        name = match[2][0]
        relation = match[0][0]
        if name not in locations :
            locations.append(name)
            newAssertions = [
                {"l":[name], "relation":relation,"r":["location"]}
            ]
            assertions.extend([x for x in newAssertions if x not in assertions])
    # matches = en.sentence.find(s, "IN NN")
    # matches += en.sentence.find(s, "TO NN")
    # ## add here and there
    # matches += en.sentence.find(s, "IN EX")
    # matches += en.sentence.find(s, "TO EX")
    # # matches += en.sentence.find(s, "IN RB")
    # # matches += en.sentence.find(s, "TO RB")
    # #matches += 
    # ####R
    # #print(matches)
    # for match in matches:
    #     name = match[1][0]
    #     relation = match[0][0]
    #     if name not in locations :
    #         locations.append(name)
    #         newAssertions = [
    #             {"l":[name], "relation":relation,"r":["location"]}
    #         ]
    #         assertions.extend([x for x in newAssertions if x not in assertions])

    # matches = en.sentence.find(s, "EX")
    # matches += en.sentence.find(s, "RB")
    # #matches += 
    # ####R
    # #print(matches)
    # for match in matches:
    #     name = match[0][0]
    #     if name not in locations :
    #         locations.append(name)
    #         newAssertions = [
    #             {"l":[name], "relation":"unknown","r":["location"]}
    #         ]
    #         assertions.extend([x for x in newAssertions if x not in assertions])

    matches = en.sentence.find(s, "or (DT) NN")
    #matches += 
    ####R
    #print(matches)
    for match in matches:
        name = match[2][0]
        if name not in locations :
            locations.append(name)
            newAssertions = [
                {"l":[name], "relation":"unknown","r":["location"]}
            ]
            assertions.extend([x for x in newAssertions if x not in assertions])

    return [locations, assertions]

####R get entities in the story.
def extract_actions(assertions, s, entities):
    #print(en.sentence.tag("Fredy is in the school"))
    entity_actions = []
    #print(entities)
    # Check for general nouns that are known names.
    #matches = en.sentence.find(s, "NN")
    
    ####R name is in NNP
    matches = en.sentence.find(s, "NN VB")
    matches += en.sentence.find(s, "NN VBZ")
    #matches += en.sentence.find(s, "NN VBZ VBG")
    matches += en.sentence.find(s, "NN VBD")
    matches += en.sentence.find(s, "NN JJ")
    #matches += en.sentence.find(s, "VBN JJ")
    #matches += en.sentence.find(s, "VBN VBD")
    ####R
    #print(matches)
    for match in matches:
        name = match[0][0]
        relation = match[1][0]
        if relation not in entity_actions :
            entity_actions.append({"S":[name], "action":relation,"O":[""]})
            newAssertions = [
                {"l":[name], "action":relation,"r":[""]}
            ]
            assertions.extend([x for x in newAssertions if x not in assertions])
    
    
    
    
    
    return [entity_actions, assertions]

def extract_possibility(assertions, s, entities):
    #print(en.sentence.tag("Fredy is in the school"))
    #possible = []
    #print(entities)
    # Check for general nouns that are known names.
    #matches = en.sentence.find(s, "NN")
    
    ####R name is in NNP
    matches = en.sentence.find(s, "or")

    for match in matches:
        #name = match[0][0]
        #relation = match[1][0]
        #if relation not in entity_actions :
        #entity_actions.append({"S":[""], "action":"change_possible_flag","O":[""]})
        newAssertions = [
            {"S":[""], "action":"change_possible_flag","O":[""]}
        ]
        assertions.extend([x for x in newAssertions if x not in assertions])
   
    return [assertions]

def extract_questions(assertions, s, question_frame_list):
    #print(type(question_frame_list))
    # if s.find("?") > 0:
    #     print(en.sentence.tag(s))

    # Check for general nouns that are known names.
    #matches = en.sentence.find(s, "NN")
    
    ####R name is in NNP
    matches = []
    argument_list = []

    for frame in question_frame_list:
        #print(type(frame))
        matches = []

        for sub_frame in frame["frame"]:
            #print(sub_frame)
            #print(type(sub_frame))
            matches += en.sentence.find(s, sub_frame)
            ####R
            #print(matches)
            for match in matches:
                #print("QQQQQQ "+s)
                name = []
                location = []
                #print(frame["name"])
                #print(frame["location"])
                if frame["name"] >= 0:
                    name = [match[int(frame["name"])][0]]
                else:
                    name = []

                if frame["location"] >=0:
                    location = [match[int(frame["location"])][0]]
                else:
                    location = []
                
                if frame["attribute"] >=0:
                    attribute = [match[int(frame["attribute"])][0]]
                else:
                    attribute = []
                if frame["verb_type"] >=0:
                    verb_type = [match[int(frame["verb_type"])][0]]
                else:
                    verb_type = []
                
                newAssertions = [
                    {"target":name, "type":"question","location":location, "verb_type": verb_type, "attribute": attribute}
                ]
                assertions.extend([x for x in newAssertions if x not in assertions])
  
    return [assertions]    
####R get entities in the story.
def extract_where_questions(assertions, s):
    #print(en.sentence.tag(s))

    # Check for general nouns that are known names.
    #matches = en.sentence.find(s, "NN")
    
    ####R name is in NNP
    matches = en.sentence.find(s, "Where VBZ DT NN")
    ####R
    #print(matches)
    for match in matches:
        name = match[3][0]
        newAssertions = [
            {"target":[name], "type":"where","r":[""]}
        ]
        assertions.extend([x for x in newAssertions if x not in assertions])

    matches = en.sentence.find(s, "Where VBZ NNP")
    ####R
    #print(matches)
    for match in matches:
        name = match[2][0]
        newAssertions = [
            {"target":[name], "type":"where","r":[""]}
        ]
        assertions.extend([x for x in newAssertions if x not in assertions])

    return [assertions]
####R get entities in the story.
def extract_yes_no_questions(assertions, s):
    #print(en.sentence.tag("? no yes from this there where Is Mary in the office "))

    # Check for general nouns that are known names.
    #matches = en.sentence.find(s, "NN")
    
    ####R name is in NNP
    matches = en.sentence.find(s, "VBZ NNP IN DT NN")
    matches += en.sentence.find(s, "VBZ NN IN DT NN")
    ####R
    #print(matches)
    for match in matches:
        #print("QQQQQQ "+s)
        name = match[1][0]
        location = match[4][0]
        newAssertions = [
            {"target":[name], "type":"question","location":[location]}
        ]
        assertions.extend([x for x in newAssertions if x not in assertions])
  
    return [assertions]
# Examples:
# The sea was unpredictable.
def extract_basic_properties(assertions, s, sp):
    matches = en.sentence.find(s, "JJ NN")
    for match in matches:
        noun = match[1][0]
        adj  = match[0][0]
        if noun!="" and adj!="":
            assertion = {"l":[noun], "relation":"has_property","r":[adj],"storypoints":[{"at":sp}]}
            if assertion not in assertions:
                assertions.append(assertion)
    return assertions

# Examples:
# Harry looked ill.
# Ariel was really happy.
def extract_actor_properties(assertions, actors, s, sp):
    matches = []
    for actor in actors:
        matches += en.sentence.find(s, actor + " is (DT) (RB) JJ")
        matches += en.sentence.find(s, actor + " was (DT) (RB) JJ")
        matches += en.sentence.find(s, actor + " looked (RB) JJ")
    for match in matches:
        actorName, adj = "", ""
        for i,m in enumerate(match):
            if m[0] in actors:
                if i==0:
                    actorName = m[0]
            elif m[1][0:2]=="JJ":
                adj = m[0]
        assertion = {"l":[actorName], "relation":"has_property","r":[adj],"storypoints":[{"at":sp}]}
        if assertion not in assertions:
            assertions.append(assertion)
    return assertions

# Examples:
#  - Ariel is an instance of mermaid.
#  - Ariel loved the land.
#  - Ariel loved Eric.
#  - Ariel gave her voice to Ursula.
#  - Ariel has the shell.
def extract_actor_actions(assertions, actors, s, sp):
    matches = []
    for actor in actors:
        # Example: Ariel (sadly) hated (the) (unpredictable) (sea).
        matches += en.sentence.find(s, actor + " (RB) VB .")
        matches += en.sentence.find(s, actor + " (RB) VB DT (JJ) NN .")
        for actor2 in actors:
            # Example: Ariel (happily) loved Eric.
            matches += en.sentence.find(s, actor + " (RB) VB " + actor2)
            # Example: Ariel (sadly) gave (her) (strong) voice to Ursula.
            matches += en.sentence.find(s, actor + " (RB) VB (PRP$) (JJ) NN to " + actor2)
    for match in matches:
        verb, actorName, actionObj, actionRecipient, pronoun, adverb = "", "", "", "", "", ""
        for i,m in enumerate(match):
            if m[1][0:2]=="VB": #or m[1][0:3]=="VBD":
                verb = m[0]
            elif m[0] in actors:
                if i==0:
                    actorName = m[0]
                elif i>=1:
                    actionRecipient = m[0]
            elif m[1][0:2]=="NN":
                actionObj = m[0]
            elif m[1][0:4]=="PRP$":
                pronoun = m[0]
            elif m[1][0:2]=="RB":
                adverb = m[0]
        if verb!="" and actorName!="":
            tense = determine_tense(verb)
            if en.verb.infinitive(verb)=="be":
                assertion = {"l":[actorName], "relation":"instance_of","r":[actionObj],"storypoints":[{"at":sp}],"tense":tense}
            else:
                assertion = {"l":[actorName], "relation":"action","r":[verb],"storypoints":[{"at":sp}],"tense":tense}
                if actionObj!="":
                    assertion["action_object"] = [actionObj]
                if actionRecipient!="":
                    assertion["action_recipient"] = [actionRecipient]
                if pronoun!="":
                    if pronoun==get_references(guess_gender(actorName))[2] or {"l":[actorName], "relation":"has_gender","r":[gender_from_reference(pronoun)]} in assertions:
                        assertion["action_object_owner"] = [actorName]
                if adverb!="" and adverb !="also" and adverb !="too":
                    assertion["with_property"] = [adverb]
            assertions.append(assertion)
    return assertions

# English honorifics and other abbreviations requiring a period.
abbreviations=["Mr.","Ms.","Mrs.","Mx.", "Mme.", "Mses.", "Mss.", "Mmes.","Dr.","St.","Messrs.","Esq.","Prof.","Jr.","Sr.","Br.","Fr.",
"Rev.","Pr.","Ph.D.","M.D.","M.S.","B.A.","B.S."]

# Split a string into a list of sentences.
def split_sentences(story):
  sentences = []
  tokens = story.split(" ")
  start = 0
  for i,t in enumerate(tokens):
    t = t.strip()
    if t.endswith("."):
      if t in abbreviations:
        continue
      else:
        sentences.append(" ".join(tokens[start:i+1]))
        start = i+1
    elif t.endswith("?") or t.endswith("!"):
      sentences.append(" ".join(tokens[start:i+1]))
      start = i+1
  if start < len(tokens):
    sentences.append(" ".join(tokens[start:]))
  return sentences

# Remove punctuation from a word.
def elim_punk(word):
  return re.sub('[:,;.?!()]', '', word)

# Determine the basic tense of a verb.
def determine_tense(verb):
    t = en.verb.tense(verb)
    if "present participle" in t:
        return "present participle"
    elif "past participle" in t:
        return "past participle"
    elif "past" in t:
        return "past"
    else:
        return "present"
