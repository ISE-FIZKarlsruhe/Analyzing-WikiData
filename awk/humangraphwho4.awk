BEGIN{prev = 0; human=5; type=31; criterion=c; criterionfound=0; humanfound=0; printing=0; i=0}
{
#Reset if value differs from previously viewed
if($1+0 != prev){
    humanfound = 0;  
    criterionfound = 0;
    printing = 0;
    i = 0;}

#Keep printing if currently viewed node has already passed all criteria (below)
if($1+0 == prev && printing==1){
    print $1";"$2";"$3} 

#save value to memory
if(printing==0){
    memory[i] = $1";"$2";"$3}

#set criterionfound values to 'true' if they are met
if($3+0 == criterion+0) criterionfound = 1;
if($3+0 == human && $2 == type) humanfound = 1;

#if all criteria are met, print the current memory and allow all further occurences to be printed
if(criterionfound==1 && humanfound==1 && printing==0){
    for (j = 0; j <= i; j++){
        print memory[j];
    }
    printing = 1}

#increment memory index    
i++;
#set previous to current
prev = $1
}