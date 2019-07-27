grammar = """
annotation =
    (set|no_set)+:d 
        ->  d
        
set = 
    begin_tag:b within_tag+:is 
         -> [b] + is
    
begin_tag = 
    ('B' '-' annotation)
    
within_tag = 
    ('I' '-' annotation)
    
no_tag = 
    O
                 
"""