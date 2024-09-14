from production import IF, AND, THEN, OR

# TODO: implement your own rules according to the defined goal tree

LUNA_GUESTS_RULES = (

    IF( OR( '(?x) floats in the air',
            '(?x) has shapeless body' ),
        THEN( '(?x) is a Lunatic' )),
    
    IF( AND( '(?x) wears jewellery',
             '(?x) has expensive accesories' ),
        THEN( '(?x) is a rich person supposedly' )),

    IF( AND( '(?x) wears baggy clothes',
             '(?x) has small luggage' ),
        THEN( '(?x) is a poor person' )),
    
    IF( AND( '(?x) is a rich person supposedly', 
            '(?x) has personal interspace vehicle'),
        THEN( '(?x) is a rich person' )),
   
    IF( AND( '(?x) is a rich person',
             '(?x) is accompanied by a very young lady' ),
        THEN( '(?x) is a Sugar Daddy' )),
   
    IF( AND( '(?x) is a rich person',
             '(?x) is live on social media' ),
        THEN( '(?x) is an Influencer' )),
    
    IF( AND( '(?x) is a rich person',
             '(?x) smokes expensive cigars' ),
        THEN( '(?x) is a Drug Dealer' )),
    
    IF( AND( '(?x) is a poor person',
             '(?x) has an addicted behavior' ),
        THEN( '(?x) is a Crypto Investor' )),
    
    IF( AND( '(?x) is a poor person', 
             '(?x) is in the group of similar looking people' ),
        THEN( '(?x) is a Student' )),
    )