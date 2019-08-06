grammar = """

# Sentence Structure
# ##################

text = 
    sentence+:d 
        ->  d

sentence = (
    differential_sentence:d  punct:p 
        -> d 
|   unmarked_token:x            punct:p 
        -> x          
)

# Normal Predicative Sentence with Distinction Pattern
# ####################################################

differential_sentence =   
    ~~(expanded_text:search_in)                        # obtain tokens with expansions
    difference_in(search_in['difference']):d           # compute the difference 
    take_all                  
        -> {'difference': d,                           
            'expansion':  search_in['expansion']}

# Elliptical Expansions
# #####################

expanded_text  = (
    expansion+:yet_parsed         
        -> myself.tokens_expansions(yet_parsed)
|   invisible_tokens:x
        -> myself.tokens_expansions([[x, [None]]])
)        

expansion = (
        except_S:x        -> x
    |   in_while_S_A_C:x  -> x
    |   the_same_A_as_S:x -> x
    |   P_than_S:x        -> x
    |   X_other_hand_X:x  -> x
)


# opposed subordinate clause
in_while_S_A_C = 
    <unmarked_token*>:a1 in_while:x <unmarked_token*>:a2 
        -> a1+a2, x
        
in_while = 
    while:m
    !(grammar_functions.subordinate_clause(m)):l
    take(l):search_in
    difference_in(search_in):d
        ->  {'difference': d,
             'expansion': [m]}
       

except_S = 
    <unmarked_token*>:a1 except:m subject:x <unmarked_token*>:a2 
        -> a1+a2, {'difference': [x],
                   'expansion': [m]}

the_same_A_as_S =
    (<(unmarked_token*)>):a1 the_same:m aspect:a as subject:s <unmarked_token*>:a2
        -> a1+a2, {'difference': [a,s],
                   'expansion': [m]}
        
P_than_S = 
    <unmarked_token*>:a1 than:m subject:x <unmarked_token*>:a2 
        -> a1+a2, {'difference': [x],
                   'expansion': [m]}
         
X_other_hand_X = 
    <unmarked_token*>:a1 other_hand:m <unmarked_token*>:a2 
        -> a1+a2, {'difference': None,
            'expansion': [m]}
        



# Difference Parts
# ################

part :what = 
    unmarked_lookahead_tokens:search_in
    ?(myself.delimit_by_match(search_in=search_in,  what=what, basic_factor=1)):p
    ?(myself.best_len(p)):l
    take(l)                
        -> p

subject = 
    part('subject'):s
        -> s      
aspect = 
    part('aspect'):s
        -> s
contrast = 
    part('contrast'):s
        -> s

difference_in :search_in =
    ?(myself.delimit_by_match(search_in=search_in, what='contrast', basic_factor=1, cant_fail=True, side_constraint='get all')):contrasts
    ?(myself.delimit_by_match(search_in=search_in, what='subject', basic_factor=3,  cant_fail=True, side_constraint='get all')):subjects
    ?(myself.delimit_by_match(search_in=search_in, what='aspect', basic_factor=0, cant_fail=True, side_constraint='get all', min_sol=True)):aspects
        ->  [subjects, contrasts, aspects]

# Markers
# #######

# CL research on comparison https://www.aclweb.org/anthology/W17-2326
# reveals high importance of these markers
# comparitive, equative, assesitive

other_hand = 
    marker(grammar_functions.other_hand_):x
        -> myself.marker_annotation('on_the_other_hand', x)  
        
than = 
    marker(grammar_functions.than_):x
        -> myself.marker_annotation('than', x)  
        
except = 
    marker(grammar_functions.except_):x
        -> myself.marker_annotation('except', x)  


the_same = 
    marker(grammar_functions.the_same_):x
        -> myself.marker_annotation('the_same', x)  

as = 
    marker(grammar_functions.as_):x
        -> myself.marker_annotation('as', x)  

while = 
     marker(grammar_functions.while_):x
    -> myself.marker_annotation('while', x)  

marker:f = 
    ~~(<anything+>:x) ?(f(x)):n take(n):y
        -> y

# indirect definiction: unmarked is anything not special
unmarked_token = 
    marker(grammar_functions.not_anything_special):y
        -> y 
      
# Basic Tokens
# ############
        
punct  = 
     marker(grammar_functions.punct_):x
        -> x
        
pseudo_sentence = 
     unmarked_token:x punct:p -> x, p

unmarked_lookahead_tokens :i = 
    ~~(<unmarked_token+>:a) 
        -> a

lookahead_tokens_no :i = 
    ~~(<unmarked_token{i}>:a) 
        -> a

invisible_tokens = 
    ~~(<non_punct+>):x
        -> x

take :i  = 
    <anything{i}>:x 
    -> x

take_all  = 
    <non_punct*>:x  
    -> x
    
non_punct = 
    anything:x ?(not grammar_functions.punct_([x])) 
        -> x

word =  
    unmarked_token:x
        -> x 
"""